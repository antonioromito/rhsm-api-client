# Red Hat RHSM APIs Python client implementation 

This project aim is to create a client interface that using Red Hat Subscription Manager (RHSM) APIs is capable to collect a series of data from your account. 

As described in the official Red Hat article [Getting started with RHSM APIs in tech preview](https://access.redhat.com/articles/3626371):

```
Using APIs in RHSM can help you more effectively keep track of and automate how you manage your Red Hat subscriptions and entitlement usage. By using APIs in RHSM, you can:

* Control which tooling you use for which products
* Better manage your system inventory
* Update and secure your systems more efficiently
* Continue receiving official support for your Red Hat products

In order to transition to using APIs for Red Hat Subscription Management, Red Hat has created a tech preview program for early access and feedback. Red Hat is in the process of decommissioning Red Hat Network (RHN), including access to its APIs. As a part of this effort, Red Hat has been developing and documenting support for RHSM.
```

## Getting Started

### Prerequisites

Red Hat Subscription Management APIs use OAuth 2.0 for authorization. For this reason rhsm-api-client uses the following libs:

* oauthlib.oauth2
* requests_oauthlib

Before to start script execution, you'll need the following information:

* Your Customer Portal credentials (https://access.redhat.com/)
* Client ID and Secret provided by Red Hat (https://access.redhat.com/management/api)
 

### Installing

Installing instruction for Fedora 29:

* Python3 package required:

    * python3-requests-oauthlib-1.0.0-1.fc29.noarch
    * python3-oauthlib-2.1.0-1.fc29.noarch

* Installation instructions:
```
$ sudo yum install python3-oauth2client
$ sudo yum install python3-requests-oauthlib
```

* Python2

    * python2-requests-oauthlib-1.0.0-1.fc29.noarch
    * python2-oauthlib-2.1.0-1.fc29.noarch

Installation instructions:
```
$ sudo yum install python2-oauth2client
$ sudo yum install python2-requests-oauthlib
```

## Deployment

This script can be executed from your preferred path

## Example Usage

$ ./get_subscriptions.py -u "MyRHNUsername" -p "MyRHNPassword" -c "MyClientID" -s "MyClientSecret" -o "systems.csv"

## Authors

* **Antonio Romito** - *Initial work* - [rhsm-api-client](https://github.com/antonioromito/rhsm-api-client)

## License

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the  GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.

