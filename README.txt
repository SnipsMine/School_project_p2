
Author: Micha Beens
Versie: 1.0.0
Datum: 18-1-2018

--------------------------------------------

Doel:
Produceren animatie alcohol-dehydrogenase

--------------------------------------------

Necessary libraries:
-shutil
-tempfile
-glob
-distutils
-math
-moviepy
-pathos
-ffmpy
-pypovray
-vapory
-numpy
-scipy
-configparser

--------------------------------------------

Necessary programs:
-Pov-Ray
-ffmpeg (in system path)

--------------------------------------------

Files:

- Alcohol_dehydrogenase.pdf
- Alcohol_2_acetaldehyde_2_azijnzuur.mp4

- default.ini
- ethanol2.pdb[1]
- models.py
- NAD.pdb[2]
- project_animation_data_ethanol_2_acetic_acid.py
- project_main.py
- project_sorted_molecules.py
- water.pdb[3]

--------------------------------------------

Usage:

Om de animatie te creëren behoren de .py documenten in de hooft pypovray map te zitten,
behalve models.py deze hoort in de pypovray map 1 stap hoger.
Het default.ini document behoort in de hooft pypovray map te zitten.
De pdb documenten horen te zitten in de pdb map.

Na de documenten op de juiste plek staan hoef je allen project_main.py te activeren en de animatie maakt zichzelf.
Als je dit doet moet je wel rekening houden dat de volledige animatie 700 frames zijn..

--------------------------------------------

Bron:

[1] https://pubchem.ncbi.nlm.nih.gov/compound/702#section=2D-Structures


[2] https://pubchem.ncbi.nlm.nih.gov/compound/5892#section=3D-Conformer
[3] default pdb file of pypovray