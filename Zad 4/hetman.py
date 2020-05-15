# -*- coding: cp1250 -*-
import datetime
import random
import statistics
import sys
import time


class Chromosome:
    def __init__(self, genes, fitness):
        self.Genes = genes
        self.Fitness = fitness


class Plansza:
    # konstruktor inicjujący szachownicę losowym położeniem hetmanów
    def __init__(self, genes, size):
        plansza = [['.'] * size for _ in range(size)]
        # konwersja str->int
        genes = [int(i) for i in genes]
        for index in range(0, len(genes), 2):
            wiersz = genes[index]
            column = genes[index + 1]
            plansza[column][wiersz] = 'H'
        self._plansza = plansza

    # rysowanie szachownicy z hetmanami
    def print(self):
        # 0,0 prints in bottom left corner
        for i in reversed(range(len(self._plansza))):
            print(' '.join(self._plansza[i]))

    # zwracamy konkretną pozycję hetmana
    def get(self, wiersz, column):
        return self._plansza[column][wiersz]


genes1 = [random.randint(0, 7) for i in range(16)]
print("Losowe współrzędne:", genes1)
plansza1 = Plansza(genes1, 8)
plansza1.print()


class Fitness:
    def __init__(self, total):
        self.Total = total

    def __gt__(self, other):
        return self.Total < other.Total

    def __ge__(self, other):
        return self.Total <= other.Total

    def __str__(self):
        return "{}".format(self.Total)


def get_fitness(genes, size):
    plansza = Plansza(genes, size)
    rowsWithHetman = set()
    colsWithHetman = set()
    northEastDiagonalsWithHetman = set()
    southEastDiagonalsWithHetman = set()
    for wiersz in range(size):
        for col in range(size):
            if plansza.get(wiersz, col) == 'H':
                rowsWithHetman.add(wiersz)
                colsWithHetman.add(col)
                northEastDiagonalsWithHetman.add(wiersz + col)
                southEastDiagonalsWithHetman.add(size - 1 - wiersz + col)
    total = size - len(rowsWithHetman) \
            + size - len(colsWithHetman) \
            + size - len(northEastDiagonalsWithHetman) \
            + size - len(southEastDiagonalsWithHetman)
    return Fitness(total)


def pokaz(candidate, startTime, size):
    timeDiff = datetime.datetime.now() - startTime
    plansza = Plansza(candidate.Genes, size)
    print(" ")
    plansza.print()
    print("Geny: {},\t fitness - {}, \tczas - {}".format(
        ' '.join(map(str, candidate.Genes)),
        candidate.Fitness,
        timeDiff))
    print(" ")


def wez_najlepsze(get_fitness, targetLen, optimalFitness, geneSet, pokaz):
    random.seed()
    naj_Rodzic = _generuj_rodzica(targetLen, geneSet, get_fitness)
    pokaz(naj_Rodzic)
    if naj_Rodzic.Fitness > optimalFitness:
        return naj_Rodzic

    # uruchom tylko na kilka sekund
    czas_dzialania = 3
    t_end = time.time() + czas_dzialania

    while time.time() < t_end:
        child = _mutacja(naj_Rodzic, geneSet, get_fitness)
        if naj_Rodzic.Fitness > child.Fitness:
            continue
        pokaz(child)

        if child.Fitness > optimalFitness:
            return child
        naj_Rodzic = child


def _generuj_rodzica(length, geneSet, get_fitness):
    genes = []
    while len(genes) < length:
        sampleSize = min(length - len(genes), len(geneSet))
        genes.extend(random.sample(geneSet, sampleSize))
    # konwersja int->str
    genes = [str(i) for i in genes]

    genes = ''.join(genes)
    fitness = get_fitness(genes)
    return Chromosome(genes, fitness)


# mutacja
def _mutacja(parent, geneSet, get_fitness):
    index = random.randrange(0, len(parent.Genes))
    childGenes = list(parent.Genes)
    newGene, alternate = random.sample(geneSet, 2)
    childGenes[index] = str(alternate) if str(newGene) == childGenes[index] else str(newGene)
    genes = ''.join(childGenes)
    fitness = get_fitness(genes)
    return Chromosome(genes, fitness)


def start(size=8):
    geneset = [i for i in range(size)]
    startTime = datetime.datetime.now()

    def fnDisplay(candidate):
        pokaz(candidate, startTime, size)

    def fnGetFitness(genes):
        return get_fitness(genes, size)

    optimalFitness = Fitness(0)
    best = wez_najlepsze(fnGetFitness, 2 * size, optimalFitness,
                    geneset, fnDisplay)


start(8)

