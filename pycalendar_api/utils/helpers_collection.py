"""
Helper functions pour grouper les collections d'Objets

* groupby_attr: Permet de grouper les listes d'Objets Python
    en passant un attribut en Chaines de caractères

* groupby_key: Permet de grouper les Iterable[dict] ou Iterable[list] en passant soit
    un key:str pour les Iterable[dict] ou key:int pour les Iterable[list]
"""
import operator as op
from collections import defaultdict
from collections.abc import Iterable, Iterator
from itertools import chain, filterfalse, tee

from more_itertools import always_iterable, map_reduce, unzip


def none_sort(iterable: Iterable, *, key: callable=None, reverse=False, none_last=True) -> Iterator:
    """Ordonne une liste d'objets python en prenant en considération Les NoneType.
    se comporte similairement au sorting de python (key and reverse) et groupe les elements
    ayant None soit au début soit vers la fin.

    N.B: La fonction est de Dimension 1 (1D), elle ne classe qu'un element/attribut à la fois
    ex: key=op.itemgetter(1, 3, 5) ou key=op.attrgetter('attr1', 'attr2', 'attr3')

    Args:

    - iterable (Iterable): Iterable (tuple, list, set, etc)
    - key (`callable`, None): fonction à appliquer aux objets ex: op.attrgetter, op.itemgetter, etc
    - reverse (`bool`, False): Ordre ascendant par défaut
    - none_last (`bool`, True): Groupe les none vers la fin par défaut, False pour les placer au début

    Returns:
        `Iterator`: `itertools.chain`, le choix de la structure de retour reste à la discretion de l'utilisateur
    """
    if key is None:
        def none_predicate(val):
            return val is None
    else:
        def none_predicate(val):
            return key(val) is None

    it1, it2 = tee(iterable, 2)
    not_nones, nones = filterfalse(none_predicate, it1), filter(none_predicate, it2)
    # Met les Nones à la fin
    if none_last:
        return chain(sorted(not_nones, reverse=reverse, key=key), nones)
    else:
        return chain(nones, sorted(not_nones, reverse=reverse, key=key))


def groupby_attr(collection: Iterable[dict|list], group_attr: Iterable[str], **kwargs) -> dict['str', Iterable]:
    """
    Groupe la collection d'objets en un Dict avec les valeurs du group_attr comme Keys

    Args:
        collection: List of objects
        group_attr: L'attribut à utiliser pour regrouper les elements.

    Returns:
        dict: Les 'keys' sont les groupes et les 'values' sont une Iterable[Item].
    """
    # Build a closure function to mimic the behavior of op.attrgetter
    getter = op.attrgetter(*always_iterable(group_attr))

    dico = defaultdict(list)
    for item in collection:
        dico[getter(item)].append(item)

    dico.default_factory = None
    return dico


def groupby_key(collection: Iterable[dict|list], group_key: Iterable[str|int]) -> dict['str', Iterable]:
    """
    Groupe la collection d'objets en un Dict avec les valeurs du group_key comme Keys

    N.B: Dans le cas d'une Iterable[list] group_key peut prendre la valeur d'un Entier (int)

    Args:
        collection: List of dict[]
        group_key: clé à utiliser pour regrouper les elements.

    Returns:
        dict: Les 'keys' sont les groupes et les 'values' une liste du dictionnaire.
    """
    getter = op.itemgetter(*always_iterable(group_key))

    dico = defaultdict(list)
    for item in collection:
        dico[getter(item)].append(item)

    dico.default_factory = None
    return dico


def _groupby(collection: list, discriminant: str, disc_getter: callable) -> dict:
    """Regroupe une collection d'objets dans un dictionnaire.

    Cette methode est meilleure que 'itertools.groupby' puisqu'elle ne nécessite
    pas que la collection soit ordonnée selon l'attribut en question.

    Args:
        collection (list): list of objects
        discriminant (str): str representation of grouping attribute.
        disc_getter (callable): a callable to access the attribute of the object.

    Returns:
        dict: a dict with keys as grouping attribute and values as list of objects of the same collection.
        i.e: a = _groupby([{'key0': 'klass1'}, {'key0': 'klass1'}, {'key0': 'klass2'}], 'key0', op.itemgetter)
        a = {'klass1': [{'key0': 'klass1'}, {'key0': 'klass1'}], 'klass2': [{'key0': 'klass2'}]}

    Raises:
        ValueError: if discriminant is not a string.
    """
    if not isinstance(discriminant, (str, int)):
        msg = f"Discriminant must be str ou int, recu: {type(discriminant)}, {discriminant}"
        raise ValueError(msg)

    if callable(disc_getter):
        dico = defaultdict(list)
        for item in collection:
            dico[disc_getter(item)].append(item)

        dico.default_factory = None
        return dico


def unzip_sum(splitted_list: list[tuple]) -> tuple:
        """Somme les valeurs présentes de chaque champs de `champs_liste` groupées par attribut

        >>> attribut = 'code_secteur'
        >>> valeurs = ['cours', 'poids']
        >>> splitted_list = [(cours_1, poids_1), (cours_2, poids_2), ..., (cours_n, poids_n)]

        Args:
            splitted_list (list[tuple]): Description

        Returns:
            tuple: somme de chaque champs
        """
        rv = [0]
        #  splitted_liste = [(cours_1, poids_1), (cours_2, poids_2), ..., (cours_n, poids_n)]
        # Unzip => [(cours_1, cours_2, ..., cours_n), (poids_1, poids_2, ..., poids_n)]
        if splitted_list:
            rv = tuple(sum(val_serie) for val_serie in unzip(splitted_list))

        return rv


def aggregate_sum_one_many(items: list[object], attribut: str, valeurs: list[str]) -> dict:
    """Somme les valeurs selon une dimension et plusieurs mesures

    Args:
        attributs (str): Dimension à utiliser
        valeurs (list[str]): Liste des mesures à sommer
    """
    keyfunc = op.attrgetter(attribut)
    valuefunc = op.attrgetter(*valeurs)

    reducefunc = unzip_sum
    rv = map_reduce(items, keyfunc, valuefunc, reducefunc)
    return rv


def aggregate_sum_many_many(self, champs_agg: list[str], champs_somme: list[str], fonction_reduction=unzip_sum) -> dict:
    """Somme les valeurs selon plusieurs dimensions et plusieurs mesures

    Args:
        champs_agg (list[str]): Liste des champs de dimension
        champs_somme (list[str]): Liste des mesures à sommer

    Returns:
         dict[tuple[champs_agg]: list[champs_somme]]:  Mapping avec tuple des dimensions et liste des mesures sommés
    """
    keyfunc = op.attrgetter(*champs_agg)
    valuefunc = op.attrgetter(*champs_somme)
    reducefunc = fonction_reduction

    rv = map_reduce(self.data, keyfunc, valuefunc, reducefunc)
    return rv
