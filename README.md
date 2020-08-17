# Mediawiki-RC-Notifier
A Nonebot plugin that provides mediawiki recent change notification, as well as manual lookup

## How to use
1. Add mediawiki_rc_lookup.py to your plugins./

1. Configure `API_PATH, SITE_NAME, TARGET_ID, PRIVATE` to ensure bot can query the api correctly and send the message to your target.

1. You may also change the scheduled job time interval as you wish. 

1. Or you may want to modify the content to your target language - there is no i18n currently, text are designed for Mandarin (zh-cn).

1. Restart your bot and enjoy!

## Abandoned
mediawiki_rc_notifier.py

mediawiki_rc_udp_server.py

These files are abandoned - no good effort of pushing notification. If you would like to help with these, you are welcome to fork and PR the changes back.
