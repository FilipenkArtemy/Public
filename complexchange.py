import numpy as np
import cmath
from PIL import Image

def Colordis(img, real, imag, oreal, oimag):
    return img[oimag][oreal] * (1 - abs(real - oreal)) * (1 - abs(imag - oimag))

def Border(shape, X0, Y0, mashtab):
    border = np.arange(X0 + 1, X0 + shape[1]) + Y0*1j
    border = np.append(border, (np.arange(X0, X0 + shape[1]) + (Y0 + shape[0])*1j))
    border = np.append(border, (np.arange(Y0, Y0 + shape[0])*1j + X0))
    return np.append(border, (np.arange(Y0, Y0 + shape[0] + 1)*1j + (X0 + shape[1])))

def Color(w, img, X0, Y0, a, b, c, d, mastab):
    if (w*c-a) != 0:
        z = ((b - d*w)/(w*c - a) - (X0 + Y0*1j))/mastab
    else:
        z = -1
    color = np.zeros(img.shape[2])
    if (img.shape[1] - 1) >= z.real >= 0 and (img.shape[0] - 1) >= z.imag >= 0:
        if z.real != int(z.real) and z.imag != int(z.imag):
            color = Colordis(img, z.real, z.imag, int(z.real), int(z.imag)) + Colordis(img, z.real, z.imag, int(z.real) + 1, int(z.imag)) + Colordis(img, z.real, z.imag, int(z.real), int(z.imag)+1) + Colordis(img, z.real, z.imag, int(z.real)+1, int(z.imag)+ 1)
        else:
            if z.real == int(z.real) and z.imag == int(z.imag):
                color = img[z.imag][z.real]
            elif z.real != int(z.real):
                color = img[z.imag][int(z.real)]*(1 - z.real + int(z.real)) + img[z.imag][int(z.real) + 1]*(z.real - int(z.real))
            else:
                color = img[int(z.imag)][int(z.real)]*(1 - z.imag + int(z.imag)) + img[int(z.imag) + 1][int(z.real)]*(z.imag - int(z.imag))
    return color

def Colorexp(w, img, X0, Y0, a, b, devexp, mastab):
    try:
        if w != 0:
            z = (cmath.log((w*devexp)/a)/b)/mastab
        else:
            z = -1
    except ValueError:
        print(w)
    color = np.zeros(img.shape[2])
    if img.shape[1] + X0 - 1 >= z.real >= X0 and img.shape[0] + Y0 - 1 >= z.imag >= Y0:
        if z.real != int(z.real) and z.imag != int(z.imag):
            color = Colordis(img, z.real, z.imag, int(z.real), int(z.imag)) + Colordis(img, z.real, z.imag, int(z.real) + 1, int(z.imag)) + Colordis(img, z.real, z.imag, int(z.real), int(z.imag)+1) + Colordis(img, z.real, z.imag, int(z.real)+1, int(z.imag)+ 1)
        else:
            if z.real == int(z.real) and z.imag == int(z.imag):
                color = img[z.imag][z.real]
            elif z.real != int(z.real):
                color = img[z.imag][int(z.real)]*(1 - z.real + int(z.real)) + img[z.imag][int(z.real) + 1]*(z.real - int(z.real))
            else:
                color = img[int(z.imag)][int(z.real)]*(1 - z.imag + int(z.imag)) + img[int(z.imag) + 1][int(z.real)]*(z.imag - int(z.imag))
    return color


def Colorlog(w, img, X0, Y0, a, b, mastab):
    z = ((cmath.exp(w/a)/b) - X0 + Y0*1j)/mastab
    color = np.zeros(img.shape[2])
    if img.shape[1] - 1 >= z.real >= 0 and img.shape[0] - 1 >= z.imag >= 0:
        if z.real != int(z.real) and z.imag != int(z.imag):
            color = Colordis(img, z.real, z.imag, int(z.real), int(z.imag)) + Colordis(img, z.real, z.imag, int(z.real) + 1, int(z.imag)) + Colordis(img, z.real, z.imag, int(z.real), int(z.imag)+1) + Colordis(img, z.real, z.imag, int(z.real)+1, int(z.imag)+ 1)
        else:
            if z.real == int(z.real) and z.imag == int(z.imag):
                color = img[z.imag][z.real]
            elif z.real != int(z.real):
                color = img[z.imag][int(z.real)]*(1 - z.real + int(z.real)) + img[z.imag][int(z.real) + 1]*(z.real - int(z.real))
            else:
                color = img[int(z.imag)][int(z.real)]*(1 - z.imag + int(z.imag)) + img[int(z.imag) + 1][int(z.real)]*(z.imag - int(z.imag))
    return color


def Mebius(path, a, b, c, d, X0 = 0, Y0 = 0, mastab = 1, cordlane = False):
    img = np.array(Image.open(path).convert('RGBA'))
    if c:
        infinity = -d/c
    else:
        infinity = X0-1
    imgborder = Border(img.shape, X0, Y0, mastab)
    if cordlane:
        for i in range(0, img.shape[1], 100):
            for k in range(img.shape[0]):
                img[k][i] = np.zeros(img.shape[2])
        for k in range(0, img.shape[0], 100):
            for i in range(img.shape[1]):
                img[k][i] = np.zeros(img.shape[2])
    if infinity in imgborder:
        imgborder = np.delete(imgborder, infinity)
    maxreal = int(max(list(map(lambda z: ((a*z+b)/(c*z+d)).real, imgborder))))+1
    minreal = int(min(list(map(lambda z: ((a*z+b)/(c*z+d)).real, imgborder))))
    maximag = int(max(list(map(lambda z: ((a*z+b)/(c*z+d)).imag, imgborder))))+1
    minimag = int(min(list(map(lambda z: ((a*z+b)/(c*z+d)).imag, imgborder))))   
    newimg = np.zeros((maximag - minimag, maxreal - minreal, img.shape[2]))
    for i in range(minreal,maxreal):
        for k in range(minimag,maximag):
            newimg[k - minimag][i - minreal] = Color(i + k*1j, img, X0, Y0, a, b, c, d, mastab)
    im = Image.fromarray(newimg.astype('uint8'))
    im.save('answer.png')
    im.show()

def Expon(path, a, b, X0 = 0, Y0 = 0, mastab = 1, cordlane = False):
    img = np.array(Image.open(path).convert('RGBA'))
    if cordlane:
        for i in range(0, img.shape[1], 100):
            for k in range(img.shape[0]):
                img[k][i] = np.zeros(img.shape[2])
        for k in range(0, img.shape[0], 100):
            for i in range(img.shape[1]):
                img[k][i] = np.zeros(img.shape[2])
    if mastab*b.real*img.shape[1] > 700:
        mastab = 700/(b*img.shape[1])
    imgborder = Border(img.shape, X0, Y0, mastab)
    maxreal = int(max(list(map(lambda z: (a*cmath.exp(z*b)).real, imgborder))))+1
    minreal = int(min(list(map(lambda z: (a*cmath.exp(z*b)).real, imgborder))))
    maximag = int(max(list(map(lambda z: (a*cmath.exp(z*b)).imag, imgborder))))+1
    minimag = int(min(list(map(lambda z: (a*cmath.exp(z*b)).imag, imgborder))))
    devexp = int(max([maxreal-minreal, maximag-minimag])/2000)
    if not devexp:
        devexp = 1
    newimg = np.zeros((int((maximag-minimag)/devexp), int((maxreal - minreal)/devexp), img.shape[2]))
    for i in range(int(minreal/devexp), int(maxreal/devexp)):
        for k in range(int(minimag/devexp),int(maximag/devexp)):
            newimg[k - int(minimag/devexp)][i - int(minreal/devexp)] = Colorexp(i + k*1j, img, X0, Y0, a, b, devexp, mastab)
    im = Image.fromarray(newimg.astype('uint8'))
    im.save('answer.png')
    im.show()

def Log(path, a, b, X0 = 0, Y0 = 0, mastab = 1, cordlane = False):
    img = np.array(Image.open(path).convert('RGBA'))
    imgborder = Border(img.shape, X0, Y0, mastab)
    if cordlane:
        for i in range(0, img.shape[1], 100):
            for k in range(img.shape[0]):
                img[k][i] = np.zeros(img.shape[2])
        for k in range(0, img.shape[0], 100):
            for i in range(img.shape[1]):
                img[k][i] = np.zeros(img.shape[2])
    if 0 in imgborder:
        imgborder.remove(0)
    maxreal = int(max(list(map(lambda z: (a*cmath.log(z*b)).real, imgborder))))+1
    minreal = int(min(list(map(lambda z: (a*cmath.log(z*b)).real, imgborder))))
    maximag = int(max(list(map(lambda z: (a*cmath.log(z*b)).imag, imgborder))))+1
    minimag = int(min(list(map(lambda z: (a*cmath.log(z*b)).imag, imgborder))))   
    newimg = np.zeros((maximag-minimag, maxreal - minreal, img.shape[2]))
    for i in range(minreal,maxreal):
        for k in range(minimag,maximag):
            newimg[k - minimag][i - minreal] = Colorlog(i + k*1j, img, X0, Y0, a, b, mastab)
    im = Image.fromarray(newimg.astype('uint8'))
    im.save('answer.png')
    im.show()

