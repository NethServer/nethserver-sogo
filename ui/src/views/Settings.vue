<template>
  <div>
    <h2>{{$t('settings.configuration')}}</h2>
    <doc-info
      :placement="'top'"
      :title="$t('docs.sogo')"
      :chapter="'sogo'"
      :section="''"
      :inline="false"
      :lang="'en'"
    ></doc-info>
    <div v-if="!view.isLoaded" class="spinner spinner-lg"></div>
    <div v-if="view.isLoaded">
      <form class="form-horizontal" v-on:submit.prevent="saveSettings('status')">
        <div :class="['form-group', errors.status.hasError ? 'has-error' : '']">
              <label
                class="col-sm-2 control-label"
                for="textInput-modal-markup"
              >{{$t('settings.status')}}</label>
              <div class="col-sm-5">
                <toggle-button
                  class="min-toggle"
                  :width="40"
                  :height="20"
                  :color="{checked: '#0088ce', unchecked: '#bbbbbb'}"
                  :value="configuration.status"
                  :sync="true"
                  @change="toggleStatus()"
                />
                <span
                  v-if="errors.status.hasError"
                  class="help-block"
                >{{errors.status.message}}</span>
              </div>
        </div>
        <div
          v-if="configuration.status"
          :class="['form-group', errors.ActiveSync.hasError ? 'has-error' : '']"
        >
          <label
            class="col-sm-2 control-label"
            for="textInput-modal-markup"
          >{{$t('settings.ActiveSync')}}</label>
          <div class="col-sm-5">
            <input type="checkbox"   true-value="enabled" false-value="disabled" v-model="configuration.ActiveSync" class="form-control">
            <span
              v-if="errors.ActiveSync.hasError"
              class="help-block"
            >{{errors.ActiveSync.message}}</span>
          </div>
        </div>
        <div
          v-if="configuration.status"
          :class="['form-group', errors.Dav.hasError ? 'has-error' : '']"
        >
          <label
            class="col-sm-2 control-label"
            for="textInput-modal-markup"
          >{{$t('settings.Dav')}}</label>
          <div class="col-sm-5">
            <input type="checkbox"   true-value="enabled" false-value="disabled" v-model="configuration.Dav" class="form-control">
            <span
              v-if="errors.Dav.hasError"
              class="help-block"
            >{{errors.Dav.message}}</span>
          </div>
        </div>
        <div
          v-if="configuration.status"
          :class="['form-group', errors.MailAuxiliaryUserAccountsEnabled.hasError ? 'has-error' : '']"
        >
          <label
            class="col-sm-2 control-label"
            for="textInput-modal-markup"
          >{{$t('settings.MailAuxiliaryUserAccountsEnabled')}}</label>
          <div class="col-sm-5">
            <input type="checkbox"   true-value="YES" false-value="NO" v-model="configuration.MailAuxiliaryUserAccountsEnabled" class="form-control">
            <span
              v-if="errors.MailAuxiliaryUserAccountsEnabled.hasError"
              class="help-block"
            >{{errors.MailAuxiliaryUserAccountsEnabled.message}}</span>
          </div>
        </div>
        <div 
          v-if="configuration.status"
          :class="['form-group', errors.AdminUsers.hasError ? 'has-error' : '']">
          <label
            class="col-sm-2 control-label"
            for="textInput-modal-markup"
          >{{$t('settings.AdminUsers')}}
          </label>
          <div class="col-sm-5">
            <textarea v-model="configuration.AdminUsers" class="form-control"></textarea>
            <span v-if="errors.AdminUsers.hasError" class="help-block">
              {{$t('validation.validation_failed')}}:
              {{$t('validation.'+errors.AdminUsers.message)}}
            </span>
          </div>
        </div>
        <div v-if="configuration.status" class="form-group">
          <legend class=" col-sm-2 control-label fields-section-header-pf" aria-expanded="true">
            <span
              :class="['fa fa-angle-right field-section-toggle-pf', advanced ? 'fa-angle-down' : '']"
            ></span>
            <a
              class="field-section-toggle-pf"
              @click="toggleAdvancedMode()"
            >{{$t('settings.advanced_mode')}}</a>
          </legend>
        </div>
        <div v-if="advanced">
          <div 
            v-if="configuration.status"
            :class="['form-group', errors.Notifications.hasError ? 'has-error' : '']">
            <label
              class="col-sm-2 control-label"
              for="textInput-modal-markup"
            >{{$t('settings.Notifications')}}
            </label>
            <div class="col-sm-5">
              <input type="checkbox" id="ACLs" value="ACLs" v-model="configuration.Notifications" class="form-control">
              <label for="ACLs">{{$t('settings.ACLs')}}</label>
              <input type="checkbox" id="Folders" value="Folders" v-model="configuration.Notifications" class="form-control">
              <label for="Folders">{{$t('settings.Folders')}}</label>
              <input type="checkbox" id="Appointment"  value="Appointment" v-model="configuration.Notifications" class="form-control">
              <label for="Appointment">{{$t('settings.Appointment')}}</label>
              <input type="checkbox" id="EMail"  value="EMail" v-model="configuration.Notifications" class="form-control">
              <label for="EMail">{{$t('settings.Email')}}</label>
              <span v-if="errors.Notifications.hasError" class="help-block">
                {{$t('validation.validation_failed')}}:
                {{$t('validation.'+errors.Notifications.message)}}
              </span>
            </div>
          </div>
          <div 
            v-if="configuration.status"
            :class="['form-group', errors.VirtualHost.hasError ? 'has-error' : '']">
            <label
              class="col-sm-2 control-label"
              for="textInput-modal-markup"
            >{{$t('settings.VirtualHost')}}
            </label>
            <div class="col-sm-5">
              <input v-model="configuration.VirtualHost" class="form-control">
              <span v-if="errors.VirtualHost.hasError" class="help-block">
                {{$t('validation.validation_failed')}}:
                {{$t('validation.'+errors.VirtualHost.message)}}
              </span>
            </div>
          </div>
          <div 
            v-if="configuration.status"
            :class="['form-group', errors.WOWorkersCount.hasError ? 'has-error' : '']">
            <label
              class="col-sm-2 control-label"
              for="textInput-modal-markup"
            >{{$t('settings.WOWorkersCount')}}
            </label>
            <div class="col-sm-5">
              <input type="number" min="1" max="200" v-model="configuration.WOWorkersCount" class="form-control">
              <span v-if="errors.WOWorkersCount.hasError" class="help-block">
                {{$t('validation.validation_failed')}}:
                {{$t('validation.'+errors.WOWorkersCount.message)}}
              </span>
            </div>
          </div>
          <div 
            v-if="configuration.status"
            :class="['form-group', errors.SOGoInternalSyncInterval.hasError ? 'has-error' : '']">
            <label
              class="col-sm-2 control-label"
              for="textInput-modal-markup"
            >{{$t('settings.SOGoInternalSyncInterval')}}
            </label>
            <div class="col-sm-5">
              <input type="number" min="1" max="60" v-model="configuration.SOGoInternalSyncInterval" class="form-control">
              <span v-if="errors.SOGoInternalSyncInterval.hasError" class="help-block">
                {{$t('validation.validation_failed')}}:
                {{$t('validation.'+errors.SOGoInternalSyncInterval.message)}}
              </span>
            </div>
          </div>
        </div>
        <div class="form-group">
          <label class="col-sm-2 control-label" for="textInput-modal-markup">
            <div v-if="loaders" class="spinner spinner-sm form-spinner-loader adjust-top-loader"></div>
          </label>
          <div class="col-sm-5">
            <button class="btn btn-primary" type="submit">{{$t('save')}}</button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: "Settings",
  components: {
  },
  mounted() {
    this.getSettings();
  },
  beforeRouteLeave(to, from, next) {
    $(".modal").modal("hide");
    next();
  },
  data() {
  return {
    view: {
      isLoaded: false
    },
    advanced: false,
    // configuration: {
    //         status: true
    // },
    loaders: false,
    errors: this.initErrors()
  };
},
methods: {
  initErrors() {
    return {
      status: {
        hasError: false,
        message: ""
      },
      ActiveSync: {
        hasError: false,
        message: ""
      },
      Dav: {
        hasError: false,
        message: ""
      },
      AdminUsers: {
          haserror: false,
          message:""
      },
      VirtualHost: {
          haserror: false,
          message:""
      },
      WOWorkersCount: {
          haserror: false,
          message:""
      },
      SOGoInternalSyncInterval: {
          haserror: false,
          message:""
      },
      MailAuxiliaryUserAccountsEnabled: {
          haserror: false,
          message:""
      },
      Notifications: {
          haserror: false,
          message:""
      }
    };
  },
  getSettings() {
    var context = this;
    context.view.isLoaded = false;
    context.advanced = false;
    
    nethserver.exec(
      ["nethserver-sogo/read"],
      {
        action: "configuration"
      },
      null,
      function(success) {
        try {
          success = JSON.parse(success);
        } catch (e) {
          console.error(e);
        }
        context.configuration = success.configuration;
        context.configuration.status = success.configuration.status == "enabled";
        context.configuration.AdminUsers = context.configuration.AdminUsers.split(",").join("\n");
        context.configuration.Notifications = context.configuration.Notifications.split(",");
        context.view.isLoaded = true;
      },
      function(error) {
        console.error(error);
          context.view.isLoaded = true;
      }
    );
  },
  toggleStatus() {
    this.configuration.status = !this.configuration.status;
    this.$forceUpdate();
  },
  saveSettings(type) {
    var context = this;
    var settingsObj = {
      action: "configuration",
      status: context.configuration.status
        ? "enabled"
        : "disabled",
        ActiveSync: context.configuration.ActiveSync,
        Dav: context.configuration.Dav,
        AdminUsers: context.configuration.AdminUsers.split("\n").join(","),
        VirtualHost: context.configuration.VirtualHost,
        WOWorkersCount: context.configuration.WOWorkersCount,
        SOGoInternalSyncInterval: context.configuration.SOGoInternalSyncInterval,
        Notifications: context.configuration.Notifications.join(","),
        MailAuxiliaryUserAccountsEnabled: context.configuration.MailAuxiliaryUserAccountsEnabled
    };
    context.loaders = true;
    context.errors = context.initErrors();
    nethserver.exec(
      ["nethserver-sogo/validate"],
      settingsObj,
      null,
      function(success) {
        context.loaders = false;
    
        // notification
        nethserver.notifications.success = context.$i18n.t(
          "settings.settings_updated_ok"
        );
        nethserver.notifications.error = context.$i18n.t(
          "settings.settings_updated_error"
        );
        // update values
        nethserver.exec(
          ["nethserver-sogo/update"],
          settingsObj,
          function(stream) {
            console.info("ddclient", stream);
          },
          function(success) {
            context.getSettings();
          },
          function(error, data) {
            console.error(error, data);
          },
          true //sudo
        );
      },
      function(error, data) {
        var errorData = {};
        context.loaders = false;
        context.errors = context.initErrors();
        try {
          errorData = JSON.parse(data);
          for (var e in errorData.attributes) {
            var attr = errorData.attributes[e];
            context.errors[attr.parameter].hasError = true;
            context.errors[attr.parameter].message = attr.error;
          }
        } catch (e) {
          console.error(e);
        }
    },
      true // sudo
  );
  },
  toggleAdvancedMode() {
    this.advanced = !this.advanced;
    this.$forceUpdate();
  }
}
};
</script>

<style>
</style>
