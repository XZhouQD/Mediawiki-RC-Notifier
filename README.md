# Mediawiki-RC-Notifier
A Nonebot plugin that provides mediawiki recent change notification

## How to use
1. IMPORTANT: Make sure you have installed nonebot scheduler function!

1. Put mediawiki_rc_udp_server.py in the same directory of your bot.py (parent directory of plugins/)

1. Configure bind address (e.g. 127.0.0.1 for localhost, 0.0.0.0 for global listening), port and site name in mediawiki_rc_udp_server.py

1. Configure your mediawiki LocalSettings.php, add the following settings:
```
$wgRCFeeds['rc'] = array(
        'formatter' => 'JSONRCFeedFormatter',
        'uri' => 'udp://{udp_server_address}:{port}',
        'omit_bots' => true,
);
```
Here, the {udp_server_address} is the address of udp server instance, and so as the port.

1. Start mediawiki_rc_udp_server.py

1. Add mediawiki_rc_notifier.py to your plugins/

1. Configure TARGET_ID and PRIVATE to let bot send notification to groups/users

1. Add mediawiki_rc_lookup.py to your plugins./

1. Configure API_PATH and SITE_NAME to ensure bot can query the api correctly

1. Restart your bot and enjoy!
