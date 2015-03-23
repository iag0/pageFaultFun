
import random
DEBUG = False

class Stream:
    def __init__( self, name, n=None ):
        self.name = name
        self.MIN = 10
        self.MAX = 100
        self.n = n if n else random.randint( self.MIN, self.MAX )
        self.sequence = [ random.randint( 1, 10 ) for _ in range( self.n ) ]
        self.i = 0
    def __len__( self ):
        return len( self.sequence )

    def rewind( self ):
        self.i = 0

    def __iter__( self ):
        return self

    def next( self ):
        if self.i < self.n:
            ret = self.sequence[ self. i ]
            self.i += 1
            return ret
        else:
            raise StopIteration()
    def printStream( self ):
        print self.sequence

class PageReplacementAlgo:
    def __init__( self, cache ):
        self.cache = cache[ : ]
    def run( self, stream ):
        self.currentWorkingStream = stream
        global DEBUG
        cc = self.cache
        n = len( cc )
        faults = 0
        for x in stream:
            if DEBUG:
                print "cache: "
                print self.cache
                print "got %d " %x,
            if x not in cc:
                faults +=1
                if DEBUG:
                    print " miss"
                self.miss( x )
            else:
                if DEBUG:
                    print " hit"
                self.hit( x )
            if DEBUG:
                print "**************"
        return faults

    def hit( self, x ):
        pass

    def miss ( self, x ):
        pass

class Random( PageReplacementAlgo ):
    def __init__( self, cache ):
        self.name = 'FIFO'
        PageReplacementAlgo.__init__( self, cache )
        self.replace = 0

    def miss( self, x ):
        index = random.randint( 0, len( self.cache ) - 1 )
        self.cache[ index ] = x

class Lru( PageReplacementAlgo ):
    def __init__( self, cache ):
        self.name = 'FIFO'
        PageReplacementAlgo.__init__( self, cache )
        self.referenceCount = [ 0 for x in self.cache ]

    def findNext( self ):
        return self.referenceCount.index( max( self.referenceCount ) )

    def tick( self ):
        for i in range( 0, len( self.referenceCount )  ):
            self.referenceCount[ i ] += 1

    def saveTick( self, index ):
        self.referenceCount[ index ] -= 1

    def miss( self, x ):
        index = self.findNext()
        self.cache[ index ] = x
        self.referenceCount[ index ] = 0
        self.tick()

    def hit( self, x ):
        index = self.cache.index( x )
        self.tick()
        self.saveTick( index )


class Fifo( PageReplacementAlgo ):
    def __init__( self, cache ):
        self.name = 'FIFO'
        PageReplacementAlgo.__init__( self, cache )
        self.replace = 0

    def miss( self, x ):
        self.cache[ self.replace ] = x
        self.replace = ( self.replace + 1 ) % len( self.cache )

class SecondChance( PageReplacementAlgo ):
    def __init__( self, cache ):
        self.name = 'SecondChance'
        PageReplacementAlgo.__init__( self, cache )
        self.referenceBits = [ 0 for x in self.cache ]

    def findNext( self ):
        for i in range( 0, len( self.referenceBits ) ):
            if self.referenceBits[ i ] == 0:
                return i
        return 0

    def hit( self, x ):
        index = self.cache.index( x )
        self.referenceBits[ index ] = 0

    def miss( self, x ):
        index = self.findNext()
        self.cache[ index ] = x
        self.referenceBits[ index ] = 1

class Optimal( PageReplacementAlgo ):
    def __init__( self, cache ):
        self.name = 'Optimal'
        PageReplacementAlgo.__init__( self, cache )

    def findNext( self ):
        nextOccurence = {}
        for c in self.cache:
            i = self.currentWorkingStream.i
            try:
                nextOccurence[ c ] = self.currentWorkingStream.sequence.index( c, i )
            except:
                nextOccurence[ c ] = 1000000
        for c in nextOccurence:
            if nextOccurence[ c ] == max( nextOccurence.values() ):
                return self.cache.index( c )

    def miss( self, x ):
        index = self.findNext()
        self.cache[ index ] = x


def test():
    stats = { 'FIFO' : 0, 'SecondChance' : 0, 'Random' : 0, 'Lru' : 0, 'OPT' : 0 }
    for _ in range( 100 ):
        thisRound = { 'FIFO' : 0, 'SecondChance' : 0, 'Random' : 0, 'Lru' : 0, 'OPT' : 0 }
        stream1 = Stream( "Stream1", 50 )
        stream1.printStream()
        cache1 = [ 1, 2, 3, 4 ]
        fifo = Fifo( cache1 )
        print "FIFO"
        faults = fifo.run( stream1 )
        print faults
        stats[ 'FIFO' ] += faults
        thisRound[ 'FIFO' ] += faults

        secondChance = SecondChance( cache1 )
        print "SecondChance"
        stream1.rewind()
        faults =  secondChance.run( stream1 )
        print faults
        stats[ 'SecondChance' ] += faults
        thisRound[ 'SecondChance' ] += faults

        randomAlgo = Random( cache1 )
        print "Random"
        stream1.rewind()
        faults = randomAlgo.run( stream1 )
        print faults
        stats[ 'Random' ] += faults
        thisRound[ 'Random' ] += faults

        lru = Lru( cache1 )
        print "Lru"
        stream1.rewind()
        faults = lru.run( stream1 )
        print faults
        stats[ 'Lru' ] += faults
        thisRound[ 'Lru' ] += faults

        optimal = Optimal( cache1 )
        print "Optimal"
        stream1.rewind()
        faults = optimal.run( stream1 )
        print faults
        stats[ 'OPT' ] += faults
        thisRound[ 'OPT' ] += faults

        print thisRound
    print stats


test()


