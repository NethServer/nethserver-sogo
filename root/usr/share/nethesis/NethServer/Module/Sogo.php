<?php
namespace NethServer\Module;


use Nethgui\System\PlatformInterface as Validate;

/**
 * Sogo Panel
 * 
 * @author stephane de Labrusse <stephdl@de-labrusse.fr>
 */
class Sogo extends \Nethgui\Controller\AbstractController
{

    protected function initializeAttributes(\Nethgui\Module\ModuleAttributesInterface $base)
    {
        return \Nethgui\Module\SimpleModuleAttributesProvider::extendModuleAttributes($base, 'Configuration', 6);
    }
    public $notificationsClasses;

    public function initialize()
    {
        $notificationsClasses = array(
            'ACLs',
            'Folders',
            'Appointment',
            'EMail'
        );
        $this->notificationsClasses = $notificationsClasses;

        $vhostValidator = $this->createValidator()->orValidator($this->createValidator(Validate::HOSTNAME_FQDN), $this->createValidator(Validate::EMPTYSTRING));

        parent::initialize();
        $this->declareParameter('status', Validate::SERVICESTATUS, array('configuration', 'sogod', 'status'));
        $this->declareParameter('ActiveSync', Validate::SERVICESTATUS, array('configuration', 'sogod', 'ActiveSync'));
        $this->declareParameter('Dav', Validate::SERVICESTATUS, array('configuration', 'sogod', 'Dav'));
        $this->declareParameter('AdminUsers', Validate::ANYTHING, array('configuration', 'sogod', 'AdminUsers'));
        $this->declareParameter('VirtualHost', $vhostValidator, array('configuration', 'sogod', 'VirtualHost'));
        $this->declareParameter('WOWorkersCount', Validate::POSITIVE_INTEGER, array('configuration', 'sogod', 'WOWorkersCount'));
        $this->declareParameter('Notifications',  Validate::ANYTHING_COLLECTION, array('configuration', 'sogod', 'Notifications', ','));
        $this->declareParameter('MailAuxiliaryUserAccountsEnabled', $this->createValidator()->memberOf('YES','NO'), array('configuration', 'sogod', 'MailAuxiliaryUserAccountsEnabled'));
    }

    public static function splitLines($text)
    {
        return array_filter(preg_split("/[,;\s]+/", $text));
    }
    public function readAdminUsers($dbList)
    {
        return implode("\r\n", explode(',' ,$dbList));
    }
    public function writeAdminUsers($viewText)
    {
        return array(implode(',', self::splitLines($viewText)));
    }

    public function validate(\Nethgui\Controller\ValidationReportInterface $report)
    {
        parent::validate($report);
        $itemValidator = $this->getPlatform()->createValidator(\Nethgui\System\PlatformInterface::USERNAME);
        foreach (self::splitLines($this->parameters['AdminUsers']) as $v) {
            if ( ! $itemValidator->evaluate($v)) {
                $report->addValidationErrorMessage($this, 'AdminUsers', 'Must be a user name', array($v));
                break;
            }
        }
    }

    public function prepareView(\Nethgui\View\ViewInterface $view)
    {
        parent::prepareView($view);
        $view['NotificationsDatasource'] = array_map(function($ac) use ($view) {
            return array($ac, $view->translate($ac . '_label'));
        }, $this->notificationsClasses);  
    }

    protected function onParametersSaved($changedParameters)
    {
        parent::onParametersSaved($changedParameters);
        $this->getPlatform()->signalEvent('nethserver-sogo-save &');
    }
}
