import numpy as np

def selectGeneSpacialCorrelation(gene, index, length):
    assert index >= 0 and len(gene) >= index + length, "gene overflow."
    return gene[index:(index+length)]

def selectGSCrandLength(gene, min_length, max_length):
    l = np.random.randint(max_length - min_length) + min_length
    index = np.random.randint(len(gene) - l - 1)
    return selectGeneSpacialCorrelation(gene, index, l), index
