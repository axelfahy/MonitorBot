# MonitorBot

> MonitorBot, the bot that warns you when your server overloads!

Send a message on the Teams' channel when a warning is raised.

## Installation

```sh
git clone https://github.com/axelfahy/MonitorBot
cd MonitorBot
python -m venv venv-dev
source venv-dev/bin/activate
pip install -e .
```

## Usage

The program is available as a CLI. Possible options are the Team's hookurl, the command to run, the threshold and the metric to use. The command must return a number, and if the number is higher than the threshold, an alert will be sent to the channel. Characters such as `|` and `$` must be escaped and the command should not contain `\` (unless for escaping), since it will be removed afterwards.

Example to send a warning when more than 80% of RAM usage is reached:

```sh
monitorbot -c "free \| grep Mem \| awk '{print $3/$2 * 100.0}'" -t 80 -m RAM
```

## Deployment

The deployment is done using Docker.

The `Dockerfile.base` file builds an image containing the requirements.

The `Dockerfile.code` file copy the code and sets the entry point.

The logs are mounted as a volume.

## Development setup

```sh
git clone https://github.com/axelfahy/MonitorBot
cd MonitorBot
python -m venv venv-dev
source venv-dev/bin/activate
pip install -r requirements_dev.txt
pip install -e .
```

## Tests

Testing is currently only checking for style and linting (`pylint`, `flake8` and `mypy`).

```sh
make test
```

## Release History

* 0.1.0
    * Initial release.

## Meta

Axel Fahy – axel@fahy.net

Distributed under the MIT license. See ``LICENSE`` for more information.

[https://github.com/axelfahy](https://github.com/axelfahy)

## Contributing

1. Fork it (<https://github.com/yourname/yourproject/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

## Version number

To set a new version:

```sh
git tag v0.1.4
git push --tags
```
