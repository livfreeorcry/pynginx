pynginx
=======

usage: pynginx [-h] [-s] [-a ADD] [-u URL] [-t TOUT] [-e ENV] [C]

Parse nginx json status page out to nagios and cacti

positional arguments:
  C                     Command to specify which data you need. Implemented:
                        Cacti Index => cacti

optional arguments:
  -h, --help            show this help message and exit
  -s, --secure           Flag https, defaults to http.
  -a ADD, --address ADD
                        hostname or ip address for the nginx host. Defaults to
                        localhost.
  -u URL, --url URL     uri path for the status page
  -t TOUT, --timeout TOUT
                        Timeout for requests in seconds
  -e ENV, --environment ENV
                        For environment specific shenanigans. dev, prod, nj.
Example:
	#./pynginx -a lb -e dev cacti
	>dev3-admin!10.2.1.77!10.2.2.77
	>qa2-sorry!10.2.1.225!10.2.2.225
	>qa-qt!10.2.1.223!10.2.2.223
	>qa-qt!10.2.1.223!10.2.2.223
	>qa2-sorry-ssl!10.2.1.225!10.2.2.225