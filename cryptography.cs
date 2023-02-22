#include <iostream>
#include <string>
#include <fstream>
#include <cryptopp/cryptlib.h>
#include <cryptopp/filters.h>
#include <cryptopp/hex.h>
#include <cryptopp/aes.h>
#include <cryptopp/osrng.h>
#include <Python.h>

using namespace std;

// Function to encrypt a file using AES encryption
bool encrypt_file(string inFilename, string outFilename, string key)
{
    // Open input and output files
    ifstream inFile(inFilename, ios::binary);
    ofstream outFile(outFilename, ios::binary);
 
    if(!inFile.is_open() || !outFile.is_open())
    {
        cout << "Error opening files!" << endl;
        return false;
    }
 
    // Generate an 16 byte key
    byte keyBytes[ CryptoPP::AES::DEFAULT_KEYLENGTH ];
    memcpy(keyBytes, key.c_str(), min(key.size(), CryptoPP::AES::DEFAULT_KEYLENGTH));
 
    // Generate a random IV
    CryptoPP::AutoSeededRandomPool prng;
    byte iv[ CryptoPP::AES::BLOCKSIZE ];
    prng.GenerateBlock( iv, CryptoPP::AES::BLOCKSIZE );
 
    // Create encryption filter
    CryptoPP::CFB_Mode< CryptoPP::AES >::Encryption cfbEncryption(keyBytes, CryptoPP::AES::DEFAULT_KEYLENGTH, iv);
 
    // Encrypt data
    CryptoPP::StreamTransformationFilter stfEncryptor(cfbEncryption, new CryptoPP::FileSink(outFile));
    inFile >> stfEncryptor;
 
    // Close files
    inFile.close();
    outFile.close();