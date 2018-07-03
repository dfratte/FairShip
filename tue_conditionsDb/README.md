# TU/e ConditionsDB for FairShip

At CERN, the European Organization for Nuclear Research, physicists and engineers are probing the fundamental structure of the universe. They use the world's largest and most complex scientific instruments to study the basic constituents of matter – the fundamental particles. The particles are made to collide together at close to the speed of light. The process gives the physicists clues about how the particles interact and provides insights into the fundamental laws of nature.

The instruments used at CERN are purpose-built particle accelerators and detectors. Accelerators boost beams of particles to high energies before the beams are made to collide with each other or with stationary targets. Detectors observe and record the results of these collisions. The SHiP experiment at a proposed new beam dump facility at the SPS will search for hidden particles as predicted by a very large number of recently elaborated models of the Hidden Sectors. These models are capable of accommodating dark matter, neutrino oscillations, and the origin of the full baryon asymmetry in the Universe. Specifically, the experiment is aimed at searching for very weakly interacting long-lived particles including Heavy Neutral Leptons - right-handed partners of the active neutrinos, vector, scalar, axion portals to the Hidden Sector, and light supersymmetric particles - sgoldstinos, etc.

The Professional Doctorate in Engineering (PDEng) degree program in Software Technology is provided by the Department of Mathematics and Computer Science of Eindhoven University of Technology in the context of the 4TU.School for Technological Design, Stan Ackermans Institute. It is an accredited and challenging two-year, Bologna Third-cycle (doctorate-level equivalent to EQF level 8) engineering degree program during which its trainees focus on strengthening their technical and non-technical competencies related to the effective and efficient design and development of software for resource-constrained software-intensive systems, such as real-time embedded or distributed systems, in an industrial setting. In particular we focus on large-scale project-based design and development of this kind of software.

In this project, the PDEng trainees are designing and implement a conditions database within the SHiP software framework. The conditions database will contain detector parameters that are necessary for the reconstruction of events and an interval of validity. After a comparative study of existing solutions in use by other experiments and collecting the user requirements from the SHiP sub detector experts, a prototype will be delivered using the most appropriate technology.

[More information about TU/e ST PDEng Program](https://www.tue.nl/en/education/tue-graduate-school/pdeng-programs/pdeng-programs-overview/pdeng-software-technology-st/)

# User Manual

## 1. Setting up the environment

Prerequisites:
 - Ubuntu 18.04
 - Python 2.7.15rc1
 - MongoDB 3.6.5 and MongoDB Compass
 - virtualenv 16.0.0

Run the following commands in a terminal to prepare the environment:
  ```bash
  $ mkdir tue_FairShip ; cd tue_FairShip
  $ git clone https://github.com/dfratte/FairShip.git
  $ git checkout mongodb
  $ cd FairShip/tue_conditionsDb/
  $ virtualenv venv
  $ . ./venv/bin/activate
  $ pip install -r resources/requirements.txt
  ```
  Database can be filled with dummy data, by running the following command
  ```bash
  $ python fill_data.py
  ```


## 2. Using the command-line interface




1. Print a help description of the CLI:
```bash
$ python cdb_cli.py -h  
```

2. List all Subdetectors from the Conditions database
```bash
$ python cdb_cli.py -ls
```

3. List all Subdetectors from the Conditions database
```bash
$ python cdb_cli.py -gas
```

4. Show all the data related to the specific Subdetector
```bash
$ python cdb_cli.py -ss "<Subdetector_name>"
```

5. Show the specific condition related to the specific Subdetector
```bash
$ python cdb_cli.py -ss "<Subdetector_name>" -sc "<Condition_name>"
```

6. Show all the data related to the specific Subdetector and then prints them into an output JSON file
```bash
$ python cdb_cli.py -ss "<Subdetector_name>" -f "<output_file_name.json>"
```

7. Retrieve a list of Conditions based on a specific tag
```bash
$ python cdb_cli.py -st "<tag_name>"
```

8. List all Global Tags from the Conditions database
```bash
$ python cdb_cli.py -lg
```
9. Add a new subdetector from a JSON file
```bash
$ python cdb_cly.py -as "<subdetector_input_file.JSON>"
```

10. Get a snapshot of Conditions based on a specific date
```bash
$ python cdb_cly.py -gs "<date>"
```
**Note:** Date should be in the following format ```"%Y,%m,%d,%H,%M,%S,%f"``` e.g. ```"2018,06,28,16,01,29,508443"```

11. Get a snapshot of Conditions based on a specific date and tags it with the global tag name
```bash
$ python cdb_cly.py -gs "<date>" -gt "<Global_Tag_name>"
```
**Note:** Date should be in the following format ```"%Y,%m,%d,%H,%M,%S,%f"``` e.g. ```"2018,06,28,16,01,29,508443"```

**Note 2:** The -f flag can be used in all commands to output the data into a JSON file.



## 3. Integrating with FairShip

It is possible to call the API from inside any python script of FairShip, by importing it. 
For example inside macro/ShipReco.py:
1. Add the following lines in any python file inside macro folder to import the API
```python
import inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from tue_conditionsDb import api
```

2. Create an instance of the API class and call its functions to fetch data from the DataBase
```python
conditionsDB_API = api.API()
conditions = conditionsDB_API.get_data_global_tag(globalTag)
```
The above command retrieves a list of conditions related to the globalTag. This list is a set of Condition objects, as defined inside `models.py`.

#### Alternatively, the code above can be applied by using the following command inside FairShip folder

```bash
$ git apply tue_conditions/resources/ShipReco.patch
```

## 4. Running tests with coverage tool
Coverage tool is used to provide insight into the percentage of code covered by unittests.

The following command should be run inside tue_conditionsDb folder:
```bash
$ coverage run -m unittest tests.test_cdb_cli tests.test_api && coverage report -m
```
**Note:** Coverage is included inside the resources/requirements.txt

## 5. Running Pylint
The pylint tool is used to make sure that PEP-8 python coding standards are enforced. It provides warnings and a score as a metric (maximum 10.0).

The following command should be run inside tue_conditionsDb folder:
```bash
$ pylint ../tue_conditionsDb/
```
**Note:** Pylint is included inside the resources/requirements.txt

## 6. Regenerating Doxygen documentation
Doxygen is used to document the code and produce a wiki page. It uses a configuration file to produce the desire output (resources/.st2017_ship_conddb_doxygen.conf)

The following command should be run inside tue_conditionsDb folder:
```bash
$ doxygen resources/.st2017_ship_conddb_doxygen.conf
```
**Note:** Doxygen can be installed in Ubuntu by running the following command in terminal:
```bash
$ sudo apt-get install doxygen
```

--------

# References
TU/e PDEng Software Technology team:

|            Member             |              Role              |             Email             |
|-------------------------------|:------------------------------:|------------------------------:|
| Ani Megerdoumian              | Project Manager                | a.megerdoumian@tue.nl         |
| Pranav Bhatnagar              | Team Leader                    | p.bhatnagar@tue.nl            |
| Beza G. Tassew                | Architect                      | b.g.tassew@tue.nl             |
| Daniel Fratte                 | Architect                      | danielrfratte@gmail.com       | 
| Dimas Satria                  | Lead Designer/Test Manager     | d.satria@tue.nl               |
| Giovanni de Almeida Calheiros | Designer/Quality Manager       | g.de.almeida.calheiros@tue.nl |
| Konstantinos Karmas           | Designer/Configuration Manager | k.karmas@tue.nl               |