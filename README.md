# Mediawiki-RC-Notifier
A Nonebot plugin that provides mediawiki recent change notification, as well as manual lookup.

The two parts: recent change notification and manual lookup are seperated into two plugins - you can use them seperately.

## How to use
### Manual Lookup
1. Add mediawiki_rc_lookup.py to your plugins/ directory.

1. Configure `API_PATH, SITE_NAME` to ensure bot can query the api correctly.

1. Restart your bot and enjoy!

### Push Notification
1. Add mediawiki_rc_notifier.py to your plugins/ directory.

1. Configure `IP, PORT, SITE_NAME, TARGET_ID, PRIVATE` to ensure bot can send updates to correct place.

1. Configure your Mediawiki in LocalSettings.php, add the following:
```
$wgRCFeeds['rc'] = array(
        'formatter' => 'JSONRCFeedFormatter',
        'uri' => 'udp://{IP}:{PORT}',
        'omit_bots' => true,
);
```
This will setup a RC Feed pushing changes through UDP to your bot, configured in mediawiki_rc_notifier.py.

1. Restart your bot and enjoy!
