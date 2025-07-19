ImageMaker NFT Platform

!!! BEFORE READING THIS DOCUMENT MAKE SURE YOU READ 'NFT_NAMING_CONVENTIONS.txt' !!!

0. Set up your Arbitrum One node provider (if having connection issues) and wallet info in the configuration file 'config.ini'.

   Note: You can use the seed phrase instead of directly passing the private key.

1. Use ImageMaker Paint (imNFTPaint) to draw an image or skip this step if you have got one.
   To clear pixel, right click on it.

   Note: ImageMaker uses a custom 16-color palette and uses 320x320 images as its tokens.
         If you have your own image drawn in an editor other than imNFTPaint,
           make sure that it is 16x16 pixel blocks in size (1 pixel block = 20x20 px square) and uses the ImageMaker palette:
           {
             0: #000000,
             1: #868686,
             2: #653600,
             3: #006500,
             4: #0000ca,
             5: #360097,
             6: #dc0000,
             7: #ffff00,

             8: #454545,
             9: #b9b9b9,
             a: #976536,
             b: #00a800,
             c: #0097ff,
             d: #ff0097,
             e: #ff6500,
             f: #ffffff
           }

2. Use ImageMaker Miner (imNFTMiner) to open the image and hit 'Mine'.
   The bar on the bottom shows you the mining progress.
   You will get .imnft token file in the end.
   It should be in the same directory as imNFTMiner.
   You can pause mining by copying already found proofs in the text area, then click 'Show Counter',
     save row iteration counter value along with the proofs somewhere.
   Then, when you want to continue mining from the previous point, load the image, paste the saved proofs,
     click 'Mine' and paste saved iteration counter, and the mining process will continue from the previous point.

   Remember: The more non-black pixels your image has,
               the more difficult it is to mine your NFT.

3. You can then set NFT info by using ImageMaker Control (imNFTControl).
   Use this program to register your NFT on blockchain,
     set owner info, manage NFT price, start/cancel auctions etc.

   Note: Check out imNFTMeta! You can upload your image to IPFS (e.g. through Pinata), copy the link to it,
           then create NFT metadata using imNFTMeta,
           and after that upload this file to IPFS again and click 'Set NFT URL' in imNFTControl.
         After all has been done, paste into the prompt the link to the .json metadata file.
         Now you can refresh metadata on your desired marketplace (Rarible, OpenSea)
           and see your token there.

4. You can buy other people's NFTs and participate in auctions using ImageMaker Client (imNFTClient).

5. 'ElProfesor.png' and 'ElProfesor.imnft' are given as examples,
     so that you can better understand the process.

   Note: ElProfesor NFT belongs to ImageMaker Foundation.
         You can still mine .imnft file from the image,
           but you cannot change NFT properties in imNFTControl.

6. In order to give away or sell your NFT directly use your crypto wallet.

Have fun mining unique NFTs!

Copyright (c) ImageMaker Foundation
