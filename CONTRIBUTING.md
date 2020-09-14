# Contributing

- [Contributing](#contributing)
  - [Preferred contributions](#preferred-contributions)
  - [Pull Request Process](#pull-request-process)
  - [Developer's guide](#developers-guide)
  - [Tests Units](#tests-units)

When contributing to this repository, please first discuss the change you wish to make via issue with the owners of this repository before making a change.

Please note we have a code of conduct, please follow it in all your interactions with the project.

## Preferred contributions

At the moment, these kind of contributions are more appreciated and should be preferred:

- Fix for issues described in [Known Issues](./README.md#known-issues)
- New cool features. Please propose your features in an issue first.
- Code optimizations: any optimization to the code is welcome

For any other kind of contribution, especially for new features, please submit an issue first.

## Pull Request Process

1. Write your code.
2. Write a **properly documentation** compliant with **reStructuredText**.
3. Write tests for your code. **Code coverage for your code must be at least at 90%**. See [Tests Units](#tests-units) to know more!
4. Report changes to the issue you opened.
5. Update the README.md and other docs with details of changes to the interface, this includes new line in the changelog, new modules if added, new command line options if added, etc.
6. Request maintainers to merge your changes.

## Developer's guide

Want to know more about how ATtila works?  
Check out the [Developers guide](docs/devwiki.md)

## Tests Units

ATtila is provided with tests units, which can be found under tests/ directory.
To launch test unit just type:

```sh
nosetests -v --with-coverage --cover-tests --cover-package=attila --nocapture tests/
```

Don't you have nose?

```sh
sudo -H pip3 install nose coverage unittest2 codecov
```

---

Thank you for any contribution! 🧡  
Christian Visintin
