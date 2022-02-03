# **F1DATA**

IP Ban count: 1

## Table of Contents
___
* [About](#about)
* [Libraries](#libraries)
* [Set Up](#set-up)
    * [Step 1: Virtual Environment Install](#step-1-virtual-environment-install)
    * [Step 2: Libraries Install](#step-2-libraries-install)
    * [Step 3: Run](#step-3)
* [Contributing](#contributing)

___
## **About**

Using [Ergast Developer API](http://ergast.com/mrd/) & [F1 Official Website](https://www.formula1.com/), build the Database for the F1 Website

<p>
Goal is to make it really easy to get the specific information each
page needs without having to write redundant code for each page

Really focus on clean organization

Ability to Update the database to the most up-to-date information when needed
</p>

___
## **Libraries**

* [VENV](https://docs.python.org/3/tutorial/venv.html)

* [Pandas](https://pandas.pydata.org/)

* [Requests](https://docs.python-requests.org/en/latest/)

* [tqdm](https://tqdm.github.io/)

* [matplotlib](https://matplotlib.org/)

___
## **Set Up**
## **Step 1: Virtual Environment Install**

**Installing Virtual Environment**

***Unix/macOS***
___


* Installing Pip
> sudo apt-get install python3-pip

* Check Installation worked
> python3 -m pip --version

* Installing Virtual Environment
> sudo apt install python3.8-venv

* Creating Virtual Environment
> python3 -m venv env

***Windows***
___

* Installing Pip
> py -m pip install --upgrade pip

* Check Installation worked
> py -m pip --version

* Installing Virtual Environment
> py -m pip install --user virtualenv

* Creating Virtual Environment
> py -m venv env

**Running Virtual Environment**

***Unix/macOS***
___
> source env/bin/activate

***Windows***
___
> .\env\Scripts\activate

**Stopping Virtual Environment**
> deactivate

___
## **Step 2: Libraries Install**

***Windows/Unix/macOS***

To install the required libraries for the program, run
> pip3 install -r requirements.txt

## **Step 3:**
### **Run**
***Unix/macOS***
> python3 `Data.py`

***Windows***
> py `Data.py`



___
## **Contributing**

* [@msebersbergerjr](https://github.com/msebersbergerjr)