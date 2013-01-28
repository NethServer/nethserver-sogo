-- SOGo Database Creation

CREATE DATABASE IF NOT EXISTS `sogo`;

CONNECT `sogo`;

CREATE TABLE IF NOT EXISTS `sogo_folder_info` (
  `c_folder_id` bigint(20) unsigned NOT NULL auto_increment,
  `c_path` varchar(255) NOT NULL,
  `c_path1` varchar(255) NOT NULL,
  `c_path2` varchar(255) default NULL,
  `c_path3` varchar(255) default NULL,
  `c_path4` varchar(255) default NULL,
  `c_foldername` varchar(255) NOT NULL,
  `c_location` varchar(2048) NOT NULL,
  `c_quick_location` varchar(2048) default NULL,
  `c_acl_location` varchar(2048) default NULL,
  `c_folder_type` varchar(255) NOT NULL,
  PRIMARY KEY  (`c_path`),
  UNIQUE KEY `c_folder_id` (`c_folder_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `sogo_user_profile` (
  `c_uid` varchar(255) NOT NULL,
  `c_defaults` text,
  `c_settings` text,
  PRIMARY KEY  (`c_uid`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

