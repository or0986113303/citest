import cv2
#import cv2.cv as cv
import numpy as np
import warnings

from Model import MTF

class Control(object):
    def __init__(self):
        self.__MTFModel__ = None
        #np.seterr(divide='ignore', invalid='ignore')
        #np.errstate(invalid='ignore')
        
    def __del__(self):
        del self.__MTFModel__
    
    def getGlobalFFTValue(self) :
        return self.__MTFModel__.globalfftvalue

    def getMTFModel(self):
        return self.__MTFModel__
    
    def setMTFModel(self, width, height):
        self.__MTFModel__ = MTF.Model(width, height)

    def setSourceImage(self, value):
        self.__MTFModel__.setSourceImage(value)
    
    def getSourceImage(self):
        return self.__MTFModel__.getSourceImage()

    def get2DDFT(self, src):
        return self.__get_2D_DFT__(src)
    
    def getESF(self, ROI):
        return self.__get_ESF__(ROI)
    
    def getLSF(self, esf):
        return self.__get_LSF__(esf)
    
    def getMTF(self , lsf):
        return self.__get_MTF__(lsf)

    def drawResult(self, img, color, ROIs, result):
        self.__draw_Result__(img, color, ROIs, result)
        
    def __draw_Result__(self, img, color, ROIs, result):
        for majorkey, subdict in ROIs.iteritems():
            cv2.putText(img, result[majorkey], (int(subdict[0]), int(subdict[1])) , cv2.FONT_HERSHEY_SIMPLEX, 1,color[majorkey], 2)

        
    def drawROIs(self, img, color, ROIs, ROIWidth, ROIHeight):
        self.__draw_ROIs__(img, color, ROIs, ROIWidth, ROIHeight)

    def __draw_ROIs__(self, img, color, ROIs, ROIWidth, ROIHeight):
        """
        Just draw the rectangle
        """
        for majorkey, subdict in ROIs.iteritems():
            cv2.rectangle(img, \
            (int(subdict[0]), int(subdict[1])), \
            (int(subdict[0] + ROIWidth), int(subdict[1] + ROIHeight)), \
            color[majorkey], 2)
        '''
        for i in range(0, ROInumbers , 1):
            cv2.rectangle(img, \
            (int(ROIData[2*i][0]), \
            int(ROIData[2*i][1])), \
            (int(ROIData[2*i + 1][0]), \
            int(ROIData[2*i + 1][1])), \
            color, 2)
        '''
        
    def __get_ESF__(self, ROI):
        """
        Edge Spread Function calculation
        """
        with np.errstate(divide='ignore', invalid='ignore'):
            X = ROI[len(ROI) - 1,:]
        #print X
            mu = np.sum(X)/X.shape[0]
            tmp = (X[:] - mu)**2
            sigma = np.sqrt(np.sum(tmp)/X.shape[0])
            edge_function = (X[:] - mu)/sigma
        
            edge_function = edge_function[::3]
        
        return edge_function
    
    def __get_LSF__(self, esf):
        """
        Line Spread Function calculation
        """
        with np.errstate(divide='ignore', invalid='ignore'):
            lsf = esf[:-2] - esf[2:]
        
        return lsf
    
    def __get_MTF__(self , lsf):
        """
        Modulation Transfer Function calculation
        """
        warnings.simplefilter('ignore', np.RankWarning)

        with np.errstate(divide='ignore', invalid='ignore'):
            mtf = abs(np.fft.fft(lsf))
            normalizemtf = mtf[:]/np.max(mtf)
        #mtf = mtf[:]/np.max(mtf)
            fitmtf = normalizemtf[:len(normalizemtf)//2]
        #mtf = mtf[:len(mtf)//2]
        #print mtf.shape[0]
        #print np.arange(mtf.shape[0])
        #print np.float32(np.arange(mtf.shape[0]) / np.float32(mtf.shape[0]))
            ix = np.arange(fitmtf.shape[0]) / np.float64(fitmtf.shape[0])
            mtf_poly =  np.polyfit(ix, fitmtf, 6)
            poly = np.poly1d(mtf_poly)
            data = [fitmtf, ix, poly]
        return data
    
    def __get_2D_DFT__(self, src):
        """
        Implement the 2D DFT method
        """
        self.__MTFModel__.globalfftvalue = 0
        h, w = src.shape[:2]
        realInput = src.astype(np.float64)
        # perform an optimally sized dft
        dft_M = cv2.getOptimalDFTSize(w)
        dft_N = cv2.getOptimalDFTSize(h)
        
        # copy A to dft_A and pad dft_A with zeros
        dft_A = np.zeros((dft_N, dft_M, 2), dtype=np.float64)
        dft_A[:h, :w, 0] = realInput
        
        # no need to pad bottom part of dft_A with zeros because of
        # use of nonzeroRows parameter in cv2.dft()
        cv2.dft(dft_A, dst=dft_A, nonzeroRows=h)
        
        # Split fourier into real and imaginary parts
        image_Re, image_Im = cv2.split(dft_A)
        
        # Compute the magnitude of the spectrum Mag = sqrt(Re^2 + Im^2)
        magnitude = cv2.sqrt(image_Re**2.0 + image_Im**2.0)
        
        # Compute log(1 + Mag)
        log_spectrum = cv2.log(1.0 + magnitude)
        
        # Rearrange the quadrants of Fourier image so that the origin is at
        # the image center
        self.__shift_dft__(log_spectrum, log_spectrum)
        
        #print np.sum(log_spectrum)
        self.__MTFModel__.globalfftvalue = np.sum(log_spectrum)
        # normalize and display the results as rgb
        cv2.normalize(log_spectrum, log_spectrum, 0.0, 1.0, 32)#)cv2.cv.CV_MINMAX)
        log_spectrum8u = (log_spectrum*255).astype('uint8')
        frame_dft = cv2.cvtColor(log_spectrum8u, cv2.COLOR_GRAY2BGR)
        return frame_dft

    def __shift_dft__(self, src , dst=None):
        """
        shift the dft by phase
        """
        if dst is None:
            dst = np.empty(src.shape, src.dtype)
        elif src.shape != dst.shape:
            raise ValueError("src and dst must have equal sizes")
        elif src.dtype != dst.dtype:
            raise TypeError("src and dst must have equal types")

        if src is dst:
            ret = np.empty(src.shape, src.dtype)
        else:
            ret = dst

        h, w = src.shape[:2]

        cx1 = cx2 = w/2
        cy1 = cy2 = h/2

        # if the size is odd, then adjust the bottom/right quadrants
        if w % 2 != 0:
            cx2 += 1
        if h % 2 != 0:
            cy2 += 1

        # swap quadrants
        # swap q1 and q3
        ret[int(h-cy1):, int(w-cx1):] = src[0:int(cy1) , 0:int(cx1) ]   # q1 -> q3
        ret[0:int(cy2) , 0:int(cx2) ] = src[int(h-cy2):, int(w-cx2):]   # q3 -> q1

        # swap q2 and q4
        ret[0:int(cy2) , int(w-cx2):] = src[int(h-cy2):, 0:int(cx2) ]   # q2 -> q4
        ret[int(h-cy1):, 0:int(cx1) ] = src[0:int(cy1) , int(w-cx1):]   # q4 -> q2

        if src is dst:
            dst[:,:] = ret

        return dst