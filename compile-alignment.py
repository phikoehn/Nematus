#!/usr/bin/python

import sys
import argparse
import numpy as np

class BPE_alignment(object):
    def __init__(self, target_fh, source_fh, alignment_fh):

        self.New_Align=[]
        Count=0

        # Loop through all lines
        while True:

            # Read lines
            target_line = target_fh.readline()
            source_line = source_fh.readline()
            alignment_line = alignment_fh.readline()
            if len(alignment_line) == 0:
              break

            Count += 1

            # Extract alignment points from string
            alignment_point=[]
            Str_pairs=alignment_line.split(' ')

            for item in Str_pairs:
                pairs=item.split('-')
                try:
                    alignment_point.append( ( int(pairs[0]),int(pairs[-1])))
                except ValueError:
                    print Count
                    print 'Value Error!'
                    sys.exit(0)

            alignment_point=sorted(alignment_point)

            # Tokenize text
            target_token = target_line.replace('\n','').split(' ')
            source_token = source_line.replace('\n','').split(' ')

            # Process BPE encoding of source tokens
            Dic={}
            for key,value in alignment_point:
                if key not in Dic:
                    Dic[key]=[value]
                else:
                    Dic[key].append(value)

            alignment_point_expanded=[]
           
            original_key=0
            for i in range(0,len(source_token)):
                
                if original_key in Dic:
                    for value in Dic[original_key]:
                        alignment_point_expanded.append((i,value))

                if len( source_token[i] )>= 2 and source_token[i][-2:]=='@@':
                    pass
                else:
                    original_key+=1

            # Now dealing with the target side
            Dic={}
            for value,key in alignment_point_expanded:
                if key not in Dic:
                    Dic[key]=[value]
                else:
                    Dic[key].append(value)

            alignment_point_final=[]
           
            original_key=0
            for i in range(0,len(target_token)):
                
                if original_key in Dic:
                    for value in Dic[original_key]:
                        alignment_point_final.append((value,i))

                if len( target_token[i] )>= 2 and target_token[i][-2:]=='@@':
                    pass
                else:
                    original_key+=1

            alignment_point_final=sorted(alignment_point_final)
            self.New_Align.append(alignment_point_final)

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', '-s', type=argparse.FileType('r'),
                        default=None, metavar='PATH', required=True,
                        help="Source file")
    parser.add_argument('--target', '-t', type=argparse.FileType('r'),
                        default=None, metavar='PATH', required=True,
                        help="Target file")
    parser.add_argument('--alignment', '-a', type=argparse.FileType('r'),
                        default=None, metavar='PATH', required=True,
                        help="Alignment file")
    parser.add_argument('--output', '-o', type=argparse.FileType('w'),
                        default=None, metavar='PATH', required=True,
                        help="Output alignment file")
    args = parser.parse_args()

    #BPE_target='data/train.bpe.ja'
    #BPE_source='data/train.bpe.en'
    #Align_file='data/train.aligned.grow-diag-final-and'

    T=BPE_alignment(args.target, args.source, args.alignment)

    np.save(args.output,np.asarray(T.New_Align))
    # 'data/train.aligned.grow-diag-final-and.npy',np.asarray(T.New_Align))

