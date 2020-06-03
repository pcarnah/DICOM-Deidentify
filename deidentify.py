# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 14:50:53 2020

@author: Patrick
"""

import pydicom
import argparse

data_elements = ['Study Description',
                 'Performed Procedure Step ID']

data_VRs = ["PN", "DA", "TM", "DT"]

data_tags = [('2001', '116C')]


def deidentify_callback(dataset, data_element):
    if data_element.VR in data_VRs or data_element.name in data_elements or data_element.tag.group == 0x0010 or data_element.tag in data_tags:
        if 'Group Length' not in data_element.name:
            data_element.value = ""


def main():
    parser = argparse.ArgumentParser(description='Deidentify DICOM data.')
    parser.add_argument('input', type=str,
                        help='The path to the input DICOM file')

    parser.add_argument('output', type=str,
                        help='The path to the output DICOM file')

    args = parser.parse_args()

    print(args.input)

    # Load dicom
    dcm = pydicom.read_file(args.input)

    dcm.walk(deidentify_callback)
    dcm.PatientID = '00000'

    dcm.save_as(args.output)

if __name__ == '__main__':
    main()