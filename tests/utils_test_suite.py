from OptoTransportAnalysis import otautils

def main():
    # Test 1 - see if can make successfully
    dict2write = {'test' : 'test!'}
    otautils.create_metadata_from_dict(dict2write)

    # Test 2 - see if giving initial directory breaks it
    otautils.create_metadata_from_dict(dict2write, initial_dir='/Users/jackbarlow/Dropbox/Jack B/data')

    print("Test complete, no errors")
    return

if __name__ == "__main__":
    main()