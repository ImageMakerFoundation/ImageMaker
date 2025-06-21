ImageMaker NFT Platform

0. Set up your Arbitrum One node provider (if having connection issues) and wallet info in the configuration file 'config.ini'.

   Note: You can use the seed phrase instead of directly passing the private key.

1. Use ImageMaker Paint (imNFTPaint) to draw an image or skip this step if you have got one.
   To clear pixel, right click on it.

   Note: ImageMaker uses a custom 16-color palette.
         If you have your own image drawn in an editor other than IMPaint,
           make sure that it is 16x16 px and uses the ImageMaker palette:
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
   It should be in the same directory as IMMiner.

   Remember: The more non-black pixels your image has,
               the more difficult it is to mine your NFT.

3. You can then set NFT info by using ImageMaker Control (imNFTControl).
   Use this program to register your NFT on blockchain,
     set owner info, manage NFT price, start/cancel auctions etc.

   Note: You can optionally set the metadata URL for your NFT
           if you want it to be readable by marketplaces like OpenSea, Rarible etc.
         More info here:
           https://docs.opensea.io/docs/metadata-standards

   Note: If you want your NFT to be reproducible locally,
           you need to add this to your metadata JSON:
         "attributes": [
           {
             "trait_type": "Name",
             "value": "<NFT filename without .imnft extension>"
           },
           {
             "trait_type": "Data",
             "value": "<Your .imnft file contents>"
           }
         ]

4. You can buy other people's NFTs and participate in auctions using ImageMaker Client (imNFTClient).

5. 'ElProfesor.png' and 'ElProfesor.imnft' are given as examples,
     so that you can better understand the process.

   Note: ElProfesor NFT belongs to ImageMaker Foundation.
         You can still mine .imnft file from the image,
           but you cannot change NFT properties in IMManager.

6. In order to give away or sell your NFT directly use your crypto wallet.

Have fun mining unique NFTs!

Copyright (c) ImageMaker Foundation
