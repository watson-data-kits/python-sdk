# Contributing

## Questions

If you are having difficulty using the APIs or have a question about Watson Data Kits,
please ask a question on [dW Answers](https://developer.ibm.com/answers/topics/watson-data-kits/).

## Issues

If you encounter an issue with the Python SDK, you are welcome to submit a [bug report](https://github.com/watson-data-kits/python-sdk/issues).
Before that, please search for similar issues. It's possible somebody has encountered this issue already.

## Pull Requests

If you want to contribute to the repository, here's a quick guide:

1. Fork the repository
1. Install `tox`
1. Run `tox -e devenv`. This will install a virtual environment with development requirements in the `venv` folder.
1. Write your code, keeping the following in mind:
    * Use the [PEP8](http://pep8.org/) coding style
    * Line length can be no more than 160 characters
    * Only python 3.6 is supported
1. Write tests and make sure all tests pass. You can simply run `tox` which will run `flake8` and `pytest`. A test report will be generated in the `coverage_html_report` folder.
1. Commit your changes
1. Push to your fork and submit a pull request to the `master` branch

## Additional Resources

* [General GitHub documentation](https://help.github.com/)
* [GitHub pull request documentation](https://help.github.com/send-pull-requests/)