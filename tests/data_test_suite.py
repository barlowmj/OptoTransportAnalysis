from OptoTransportAnalysis.Transport import TransportData
from OptoTransportAnalysis.Optics import OpticsData
import OptoTransportAnalysis as ota
import OptoTransportAnalysis.Transport as td
import OptoTransportAnalysis.Optics as od

def main():
    # first test: check if user input works to instantiate TransportData object by comparing filename
    testData = TransportData()
    print(f'Filename of testData object is {testData.filename}')
    match = input('Does this match the chosen filename? y/n')
    assert(match == 'y'), 'Chosen filename does not match testData filename'

    # second test: check if user input works to instantiate OpticsData object by comparing filename
    testData = OpticsData()
    print(f'Filename of testData object is {testData.filename}')
    match = input('Does this match the chosen filename? Enter \'y\' if so')
    assert(match == 'y'), 'Chosen filename does not match testData filename'

    # third test: check if giving filename in argument works
    testFile = '/Users/jackbarlow/Dropbox/Jack B/data/ISBT/Stencil mask 10L & EBL 11L/bluefors 20220909/databases/52_ISBT_0928_DCBiasSweep_2fTest.db'
    testData = TransportData(testFile)
    assert(testData.filename == testFile), 'testData filename does not match testFile'

    print("Test complete, no errors")
    return

if __name__ == "__main__":
    main()