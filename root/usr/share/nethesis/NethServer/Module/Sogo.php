<?php
namespace NethServer\Module;

/*
 * Copyright (C) 2018 Nethesis S.r.l.
 *
 * This script is part of NethServer.
 *
 * NethServer is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * NethServer is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with NethServer.  If not, see <http://www.gnu.org/licenses/>.
 */


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


        parent::initialize();
        $this->declareParameter('status', Validate::SERVICESTATUS, array('configuration', 'sogod', 'status'));
        $this->declareParameter('ActiveSync', Validate::SERVICESTATUS, array('configuration', 'sogod', 'ActiveSync'));
        $this->declareParameter('Dav', Validate::SERVICESTATUS, array('configuration', 'sogod', 'Dav'));
        $this->declareParameter('AdminUsers', Validate::ANYTHING, array('configuration', 'sogod', 'AdminUsers'));
        $this->declareParameter('VirtualHost', Validate::ANYTHING, array('configuration', 'sogod', 'VirtualHost'));
        $this->declareParameter('WOWorkersCount', $this->createValidator(Validate::POSITIVE_INTEGER)->lessThan(201), array('configuration', 'sogod', 'WOWorkersCount'));
        $this->declareParameter('SOGoInternalSyncInterval',$this->createValidator(Validate::POSITIVE_INTEGER)->lessThan(61), array('configuration', 'sogod', 'SOGoInternalSyncInterval'));
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

    public function readVirtualHost($dbList)
    {
        return implode("\r\n", explode(',' ,$dbList));
    }
    public function writeVirtualHost($viewText)
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
        $hostValidator = $this->getPlatform()->createValidator(\Nethgui\System\PlatformInterface::HOSTNAME_FQDN);
        foreach (self::splitLines($this->parameters['VirtualHost']) as $v) {
            if ( ! $hostValidator->evaluate($v)) {
                $report->addValidationErrorMessage($this, 'VirtualHost', 'Must be a valid FQDN', array($v));
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
