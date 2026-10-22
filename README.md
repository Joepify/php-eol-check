# php-eol-check

See which **PHP version** a website exposes and whether that branch still gets **security fixes**. One Python file, no dependencies. Latest patch versions come live from php.net (`/releases/active.php`); end-of-support dates from [php.net/supported-versions](https://www.php.net/supported-versions.php) (checked 22 Oct 2026).

```bash
python3 php_eol_check.py https://example.nl
python3 php_eol_check.py example.nl --json
```

Statuses: `supported`, `outdated-patch` (branch supported, but a newer security release exists), `end-of-life` (PHP 8.1 and older), `unknown` (version hidden, which is good practice).

| Branch | Security fixes until |
|---|---|
| 8.2 | 31 Dec 2026 |
| 8.3 | 31 Dec 2027 |
| 8.4 | 31 Dec 2028 |
| 8.5 | 31 Dec 2029 |

Note: many hosts hide `X-Powered-By`; then ask your host which version runs. Running WordPress? Guide (Dutch): https://www.joepify.nl/kennisbank/php-versie-wordpress

Made by [Joepify](https://www.joepify.nl), Rotterdam. MIT licence.
