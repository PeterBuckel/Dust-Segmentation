# Dust-Segmentation
Labeling and Segmentation of Dust

##  Deep learning based semantic segmentation of dust
VGG-Unet Model 
`model.py`
[Trained Models](https://choosealicense.com/licenses/mit/)

Dust Segmentation Dataset: [Trained Models](https://choosealicense.com/licenses/mit/)
Folder Structure

    dust_segmentation.zip
    ├── DCP-labeled             # Labeled by the DCP method with the GUI
    │   ├── test                # Test dataset labeled by the DCP method with the GUI
    │   │   ├── images
    │   │   ├── masks
    ├── Hand-labeled            # Labeled by handthe DCP method with the GUI
    │   ├── train_val           # Training and Valiation images and masks
    │   │   ├── images
    │   │   ├── masks
    │   ├── test                # Test images and masks
    │   │   ├── images
    │   └── └── masks
    └── ...


##  GUI Dust Labeling
Hier noch text



![GUI](figures/gui.png)

Input image            |  Output mask
:-------------------------:|:-------------------------:
![input](figures/input_image.png)  |  ![output](output/mask.png)

## License
<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.

## Citation
