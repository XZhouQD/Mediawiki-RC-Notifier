<div align="center">
<h1>Mediawiki-RC-Notifier</h1>

### A Nonebot plugin that provides mediawiki recent change notification, as well as manual lookup.

[![](https://img.shields.io/github/license/XZhouQD/Mediawiki-RC-Notifier?style=for-the-badge)](https://github.com/XZhouQD/Mediawiki-RC-Notifier/blob/master/LICENSE)
![Mediawiki Version](https://img.shields.io/badge/Mediawiki-1.25.0+-yellow.svg?style=for-the-badge)
[![Nonebot Version](https://img.shields.io/badge/nonebot-1.7.0+-green.svg?style=for-the-badge)](https://pypi.python.org/pypi/nonebot)
![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg?style=for-the-badge)
![CQHTTP Version](https://img.shields.io/badge/cqhttp-4.8+-black.svg?style=for-the-badge)

</div>

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
