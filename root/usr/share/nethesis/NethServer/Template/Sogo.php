<?php

/* @var $view Nethgui\Renderer\Xhtml */

echo $view->header()->setAttribute('template', $T('Sogo_header'));

echo $view->panel()->insert($view->fieldsetSwitch('status', 'enabled',$view::FIELDSETSWITCH_CHECKBOX | $view::FIELDSETSWITCH_EXPANDABLE)->setAttribute('uncheckedValue', 'disabled')

        ->insert($view->checkBox('Dav', 'enabled')->setAttribute('uncheckedValue', 'disabled'))
        ->insert($view->checkBox('ActiveSync', 'enabled')->setAttribute('uncheckedValue', 'disabled'))
        ->insert($view->checkBox('MailAuxiliaryUserAccountsEnabled', 'YES')->setAttribute('uncheckedValue', 'NO'))
        ->insert($view->textArea('AdminUsers', $view::LABEL_ABOVE)->setAttribute('dimensions', '5x30'))

        ->insert($view->fieldset(NULL, $view::FIELDSET_EXPANDABLE)->setAttribute('template', $T('Notifications_label'))
            ->insert($view->selector('Notifications', $view::SELECTOR_MULTIPLE| $view::LABEL_NONE))
        )

        ->insert($view->fieldset(NULL, $view::FIELDSET_EXPANDABLE)->setAttribute('template', $T('Advanced_label'))
            ->insert($view->textInput('VirtualHost'))
            ->insert($view->textInput('WOWorkersCount'))
            ->insert($view->textInput('SOGoInternalSyncInterval'))
        )
);

echo $view->buttonList($view::BUTTON_SUBMIT | $view::BUTTON_HELP);
