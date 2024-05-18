export const variantsIni = `
# Hybrid variant of Grand-chess and crazyhouse, using Grand-chess as a template
[grandhouse:grand]
startFen = r8r/1nbqkcabn1/pppppppppp/10/10/10/10/PPPPPPPPPP/1NBQKCABN1/R8R[] w - - 0 1
pieceDrops = true
capturesToHand = true

# Hybrid variant of Gothic-chess and crazyhouse, using Capablanca as a template
[gothhouse:capablanca]
startFen = rnbqckabnr/pppppppppp/10/10/10/10/PPPPPPPPPP/RNBQCKABNR[] w KQkq - 0 1
pieceDrops = true
capturesToHand = true

# Hybrid variant of Embassy chess and crazyhouse, using Embassy as a template
[embassyhouse:embassy]
startFen = rnbqkcabnr/pppppppppp/10/10/10/10/PPPPPPPPPP/RNBQKCABNR[] w KQkq - 0 1
pieceDrops = true
capturesToHand = true

[gorogoroplus:gorogoro]
startFen = sgkgs/5/1ppp1/1PPP1/5/SGKGS[LNln] w 0 1
lance = l
shogiKnight = n
promotedPieceType = l:g n:g

[shogun:crazyhouse]
startFen = rnb+fkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNB+FKBNR[] w KQkq - 0 1
commoner = c
centaur = g
archbishop = a
chancellor = m
fers = f
promotionRegionWhite = *6 *7 *8
promotionRegionBlack = *3 *2 *1
promotionLimit = g:1 a:1 m:1 q:1
promotionPieceTypes = -
promotedPieceType = p:c n:g b:a r:m f:q
mandatoryPawnPromotion = false
firstRankPawnDrops = true
promotionZonePawnDrops = true
whiteDropRegion = *1 *2 *3 *4 *5
blackDropRegion = *4 *5 *6 *7 *8
immobilityIllegal = true

[orda:chess]
centaur = h
knibis = a
kniroo = l
silver = y
promotionPieceTypes = qh
startFen = lhaykahl/8/pppppppp/8/8/8/PPPPPPPP/RNBQKBNR w KQ - 0 1
flagPiece = k
flagRegionWhite = *8
flagRegionBlack = *1

[synochess:pocketknight]
janggiCannon = c
soldier = s
horse = h
fersAlfil = e
commoner = a
startFen = rneakenr/8/1c4c1/1ss2ss1/8/8/PPPPPPPP/RNBQKBNR[ss] w KQ - 0 1
stalemateValue = loss
perpetualCheckIllegal = true
flyingGeneral = true
blackDropRegion = *5
flagPiece = k
flagRegionWhite = *8
flagRegionBlack = *1

[shinobi:crazyhouse]
commoner = c
bers = d
archbishop = j
fers = m
shogiKnight = h
lance = l
promotionRegionWhite = *7 *8
promotionRegionBlack = *2 *1
promotionPieceTypes = -
promotedPieceType = p:c m:b h:n l:r
mandatoryPiecePromotion = true
stalemateValue = loss
nFoldRule = 4
perpetualCheckIllegal = true
startFen = rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/LH1CK1HL[LHMMDJ] w kq - 0 1
capturesToHand = false
whiteDropRegion = *1 *2 *3 *4
immobilityIllegal = true
flagPiece = k
flagRegionWhite = *8
flagRegionBlack = *1

[shinobiplus:crazyhouse]
commoner = c
bers = d
dragonHorse = f
archbishop = j
fers = m
shogiKnight = h
lance = l
promotionRegionWhite = *7 *8
promotionRegionBlack = *1 *2 *3
promotionPieceTypes = -
promotedPieceType = p:c m:b h:n l:r
mandatoryPiecePromotion = true
stalemateValue = loss
nFoldRule = 4
perpetualCheckIllegal = true
startFen = rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/4K3[JDFCLHM] w kq - 0 1
capturesToHand = false
whiteDropRegion = *1 *2 *3 *4
immobilityIllegal = true
flagPiece = k
flagRegionWhite = *8
flagRegionBlack = *1

[ordamirror:chess]
centaur = h
knibis = a
kniroo = l
customPiece1 = f:mQcN
promotionPieceTypes = lhaf
startFen = lhafkahl/8/pppppppp/8/8/PPPPPPPP/8/LHAFKAHL w - - 0 1
flagPiece = k
flagRegionWhite = *8
flagRegionBlack = *1

[empire:chess]
customPiece1 = e:mQcN
customPiece2 = c:mQcB
customPiece3 = t:mQcR
customPiece4 = d:mQcK
soldier = s
promotionPieceTypes = q
startFen = rnbqkbnr/pppppppp/8/8/8/PPPSSPPP/8/TECDKCET w kq - 0 1
stalemateValue = loss
nFoldValue = win
flagPiece = k
flagRegionWhite = *8
flagRegionBlack = *1
flyingGeneral = true

[chak]
maxRank = 9
maxFile = 9
rook = r
knight = v
centaur = j
immobile = o
customPiece1 = s:FvW
customPiece2 = q:pQ
customPiece3 = d:mQ2cQ2
customPiece4 = p:fsmWfceF
customPiece5 = k:WF
customPiece6 = w:FvW
startFen = rvsqkjsvr/4o4/p1p1p1p1p/9/9/9/P1P1P1P1P/4O4/RVSJKQSVR w - - 0 1
mobilityRegionWhiteCustomPiece6 = *5 *6 *7 *8 *9
mobilityRegionWhiteCustomPiece3 = *5 *6 *7 *8 *9
mobilityRegionBlackCustomPiece6 = *1 *2 *3 *4 *5
mobilityRegionBlackCustomPiece3 = *1 *2 *3 *4 *5
promotionRegionWhite = *5 *6 *7 *8 *9
promotionRegionBlack = *5 *4 *3 *2 *1
promotionPieceTypes = -
mandatoryPiecePromotion = true
promotedPieceType = p:w k:d
extinctionValue = loss
extinctionPieceTypes = kd
extinctionPseudoRoyal = true
flagPiece = d
flagRegionWhite = e8
flagRegionBlack = e2
nMoveRule = 50
nFoldRule = 3
nFoldValue = draw
stalemateValue = loss

[chennis]
maxRank = 7
maxFile = 7
mobilityRegionWhiteKing = b1 c1 d1 e1 f1 b2 c2 d2 e2 f2 b3 c3 d3 e3 f3 b4 c4 d4 e4 f4
mobilityRegionBlackKing = b4 c4 d4 e4 f4 b5 c5 d5 e5 f5 b6 c6 d6 e6 f6 b7 c7 d7 e7 f7
customPiece1 = p:fmWfceF
cannon = c
commoner = m
fers = f
soldier = s
king = k
bishop = b
knight = n
rook = r
promotionPieceTypes = -
promotedPieceType = p:r f:c s:b m:n
promotionRegionWhite = *1 *2 *3 *4 *5 *6 *7
promotionRegionBlack = *7 *6 *5 *4 *3 *2 *1
startFen = 1fkm3/1p1s3/7/7/7/3S1P1/3MKF1[] w - 0 1
pieceDrops = true
capturesToHand = true
pieceDemotion = true
mandatoryPiecePromotion = true
dropPromoted = true
castling = false
stalemateValue = loss

# Mansindam (Pantheon tale)
# A variant that combines drop rule and powerful pieces, and there is no draw
[mansindam]
variantTemplate = shogi
pieceToCharTable = PNBR.Q.CMA.++++...++Kpnbr.q.cma.++++...++k
maxFile = 9
maxRank = 9
pocketSize = 8
startFen = rnbakqcnm/9/ppppppppp/9/9/9/PPPPPPPPP/9/MNCQKABNR[] w - - 0 1
pieceDrops = true
capturesToHand = true
shogiPawn = p
knight = n
bishop = b
rook = r
queen = q
archbishop = c
chancellor = m
amazon = a
king = k
commoner = g
centaur = e
dragonHorse = h
bers = t
customPiece1 = i:BNW
customPiece2 = s:RNF
promotionRegionWhite = *7 *8 *9
promotionRegionBlack = *3 *2 *1
mandatoryPiecePromotion = true
doubleStep = false
castling = false
promotedPieceType = p:g n:e b:h r:t c:i m:s
dropNoDoubled = p
stalemateValue = loss
nMoveRule = 0
nFoldValue = win
flagPiece = k
flagRegionWhite = *9
flagRegionBlack = *1
immobilityIllegal = true

[paradigm30]
maxRank = 8
maxFile = 8
pawn = p
king = k
queen = q
rook = r
knight = n
customPiece1 = d:BnN
promotionPieceTypes = ndrq
promotionRegionWhite = *8
promotionRegionBlack = *1
startFen = rndqkdnr/pppppppp/8/8/8/8/PPPPPPPP/RNDQKDNR w KQkq - 0 1

[sandbox]
maxRank = 8
maxFile = 8
pawn = p
king = k
queen = q
rook = r
bishop = b
knight = n
archbishop = c
chancellor = m
amazon = a
commoner = d
fers = f
wazir = w
centaur = g
customPiece1 = u:NN
customPiece2 = h:gRgB
customPiece3 = o:mfFcfeWimfB2
customPiece4 = s:feFfeWimfnD
customPiece5 = l:WFNAD
pawnTypes = ops
promotionPieceTypes = nbrqcmadguhl
promotionRegionWhite = *8
promotionRegionBlack = *1
startFen = rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
nFoldRule = 3
nFoldValue = draw
nMoveRule = 50

[fairyland:chess]
chancellor = y
customPiece1 = f:fWmfFimfnD
customPiece2 = a:AD
customPiece3 = u:BfR
customPiece4 = g:RFA
customPiece5 = w:FfW
promotionPieceTypesBlack = awuyg
pawnTypes = pf
flagPiece = k
flagRegionWhite = a7 b7 g7 h7
flagRegionBlack = -
promotionRegionWhite = *8 a7 b7 g7 h7
promotionRegionBlack = *1 a2 b2 g2 h2
startFen = awuykgwa/ffffffff/8/8/8/8/PPPPPPPP/RNBQKBNR w KQ - 0 1

[randomized:chess]
archbishop = c
chancellor = m
amazon = a
centaur = g
commoner = d
bers = i
dragonHorse = h
gold = l
customPiece1 = o:WFAD
customPiece2 = w:WFD
customPiece3 = y:WD
customPiece4 = u:BWN
customPiece5 = v:RFN
promotionPieceTypes = ao
startFen = rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/4K3 w kq - 0 1

[rand2:chess]
chess960 = true
shogiPawn = s
bers = d
dragonHorse = h
archbishop = a
chancellor = c
amazon = z
commoner = g
fersAlfil = f
cannon = o
centaur = u
customPiece1 = e:mfFcfeWifmnA
customPiece2 = t:fF
customPiece3 = m:WFAND
customPiece4 = i:W3F3
customPiece5 = w:WD
customPiece6 = v:mBcpB
customPiece7 = l:AD
customPiece8 = j:C
customPiece9 = x:NN
customPiece10 = y:fBbR
castlingRookPieces = rdhiux
pawnTypes = pset
promotionPieceTypes = q
startFen = 4k3/8/8/8/8/8/8/4K3 w KQkq - 0 1

[ordarandom:ordamirror]
silver = y
amazon = m
customPiece2 = t:mNcK
customPiece3 = c:mNcQ
customPiece4 = g:mKcN
customPiece5 = o:KNA
customPiece6 = d:mKcB
customPiece7 = s:mKcR
customPiece8 = v:KsD
customPiece9 = w:mBcR
customPiece10 = x:mRcB
customPiece11 = i:mQcKcN
customPiece12 = z:mRcKcD
startFen = lhafkahl/8/pppppppp/8/8/PPPPPPPP/8/4K3 w - - 0 1
promotionPieceTypes = hm

[shinogi:shogi]
pawn = o
commoner = c
archbishop = j
fers = m
customPiece1 = f:BW
mandatoryPawnPromotion = false
promotedPieceType = o:g m:g f:j
startFen = bcmgkgsnl/1r5f1/ooooppppp/9/9/9/PPPPPOOOO/1F5R1/LNSGKGMCB[-] w - - 0 1`
