# recipe
```recipe``` is a small python script used to read multiple recepies from a simple file format, scale them to a certain number of persons/portions converting units acordingly and create a pdf using LaTeX.

## Getting Started
install following dependencies:
* LaTeX https://www.latex-project.org/
* Python https://www.python.org/

run sample.py
```
py sample.py
```
or
```
python sample.py
```
## Recipe File Format
The recipe file format contains multipile different textblocks sperated by one empty new line. There are two different kind of textblocks and textblocks can be in any possible order.

### Header
Contains information about recipe.

#### Example
```
[Amerikanische Pfirsiche]
time: 1h
device: Pfanne
persons: 4
```

#### Format
``` [title] ```
Title of recipe, title can contain any unicode letters including ',- and whitespaces

```variable: value```
Allowed variables are:
* **time** time it will take someone to make this recipe
* **device** the device you cook this recipe with
* **persons** the number of persons this recipe is going to serve

### Instruction
Contains one text instruction with ingredients used during this instruction.

#### Example
```
>300.0 ml Wasser
>4.0 EL Zitronensaft
>2.0 Nelke/Nelken
> etwas Zimt
>0.25 TL Ingwer
weichkochen
```

#### Format
```
>quantity unit name/pluralname
>quantity name/pluralname
> name/pluralname
```
Allowed variables are:
* **quantity** a number, can be 1-2, optional
* **unit** can contain any unicode letters, optional
* **name** can contain any unicode letters including :,- and whitespaces
* **pluralname** same as name, optional

Everything in an instruction block not matching an ingredient will be added to the instructions. 

## Set Number Of Persons
persons.txt contains several lines, which determine the factor in which the recipes are to be scaled

### Default Factor
Factor in which every recipe is scaled, if no specific factor is given. First entry of the file

#### Format
```
[persons]factor
```
Allowed variables are:
* **factor** a number

### Specific Factor
Factor in which one single recipe is scaled.

#### Format
```
[title]factor
```
Allowed variables are:
* **title** Title of recipe, title can contain any unicode letters including ',- and whitespaces
* **factor** a number

## Fixes
If there is no unit, but the ingredient starts with lowercase, the program will recognize the ingredient as unit. To prevent this, change 
>(2) ingredient 
to 
>(2) n ingredient 
