//Get title and path
titleOrig = getTitle();
title = titleOrig.substring(0, titleOrig.length() - 4);
path_temp = File.directory();
path = path_temp.substring(0, path_temp.length()-1);

//Split channels
run("Split Channels");

//RFP channel is C1
selectWindow("C1-" + titleOrig);
run("Z Project...", "projection=[Max Intensity]");
saveAs("Tiff", path + "\\" + title + "-RFP.tif");

//GFP channel is C2
selectWindow("C2-" + titleOrig);
run("Z Project...", "projection=[Max Intensity]");
saveAs("Tiff", path + "\\" + title + "-GFP.tif");

//BFP channel is C3
selectWindow("C3-" + titleOrig);
run("Z Project...", "projection=[Max Intensity]");
saveAs("Tiff", path + "\\" + title + "-BFP.tif");

//Brightfield channel is C4
selectWindow("C4-" + titleOrig);
run("Z Project...", "projection=[Max Intensity]");
saveAs("Tiff", path + "\\" + title + "-bright.tif");

//Close all images
close("*");;