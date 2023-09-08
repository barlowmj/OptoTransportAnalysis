# OptoTransportAnalysis

## Project description
Data analysis infrastructure for work in Xu lab @ UW across optical and transport measurements.

## Instructions for installing `OptoTransport` conda environment
This repository contains an `environment.yml` file, which directs conda to create an environment with all necessary packages to make this package work. You can install the environment using the following steps:
1. Step into the directory where the `environment.yml` file is stored.
2. Create the environment by running `$ conda env create -f environment.yml`
3. Activate the environment by running `$ conda activate OptoTransport`

More info on conda and activating environments:
* Installing conda: https://learning.anaconda.cloud/?utm_campaign=starter-mktg&utm_medium=online-advertising&utm_source=google&gclid=CjwKCAiA-dCcBhBQEiwAeWidtVqZ-CXpReEyQC5J6LUkmnVll_6RWkciK_s15SbfN0mTBgxQ5lMuPRoCn3AQAvD_BwE
* Activating environments using .yml files: https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html

## Updating your conda environment:
1. Update `environment.yml` file with desired packages by adding them to the list of packages under `dependencies`.
2. Activate the `OptoTransport` environment and step into the directory where `environment.yml` is saved.
3. Update the environment by running `$ conda env update --file environment.yml --prune`

Updating conda environments can be very slow. For faster performance, you can install mamba (more info: https://anaconda.org/conda-forge/mamba) and run the above command using `$ mamba` instead of `$ conda`.

## Installing the `OptoTransportAnalysis` library
In order to use the library/module from anywhere on your machine while using the `OptoTransport` environment, you need to install the package using pip while in this environment:
1. Step into the highest level of the `OptoTransportAnalysis` package in your command line. This highest level should contain the `pyproj.toml` file, which communicates to the installer the details of the package.
2. Activate the `OptoTransport` environment.
3. Install the package to this environment by running `$ pip install --no-deps --editable . --config-settings editable_mode=strict`, where `--no-deps` tells pip to not install the dependencies and `-e` allows the package to be updated as it continues to be worked on without having to re-install each time an edit is made. The `--config-settings` prompt is a recommendation from Stack Exchange to make importing editable packages in VSCode less annoying (https://stackoverflow.com/questions/76213501/python-packages-imported-in-editable-mode-cant-be-resolved-by-pylance-in-vscode).
You can now import functions and TransportData/OpticsData objects from this library using the statement `import OptoTransportAnalysis` when running a file in the `OptoTransport` conda environment!

### More info on packaging in `python`:
Coming soon!