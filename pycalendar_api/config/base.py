import tomllib
from dataclasses import asdict, dataclass, fields
from pathlib import Path
from typing import ClassVar, Self

import tomlkit as tk

from .constants import CONSTANTS
from .exceptions import ConfigurationError
from .utils import dict_to_toml, toml_doc_to_dict


@dataclass
class ConfigSection:
    section: ClassVar[str] = 'root'
    key: ClassVar[str|None] = None
    encoding: ClassVar[str] = CONSTANTS.ENCODING
    appname: ClassVar[str] = CONSTANTS.APPLICATION_NAME

    def duplicate(self) -> Self:
        return self.__class__(**asdict(self))

    def get_sections(self) -> list["ConfigSection"]:
        rv = [getattr(self, f.name) for f in fields(self) if issubclass(f.type, ConfigSection)]
        return rv

    def save_current_config(self, fpath: str|Path, *, sort_keys: bool=False, include_section: bool=True):
        fpath = Path(fpath)
        dico = dict_to_toml(asdict(self))
        try:
            if include_section and self.section != 'root':
                dico = {self.section: dico}
            fpath.write_text(tk.dumps(dico, sort_keys=sort_keys), encoding=self.encoding)
            msg = f"Configuration de {self.section} sauvegardée dans le fichier -> {fpath}"
            print(msg)
        except tk.exceptions.TOMLKitError as err:
            raise ConfigurationError(err)

    @classmethod
    def from_config_file(cls, fpath: str|Path, *, with_section: bool=True) -> "ConfigSection":
        """Charge la configuration depuis un fichier toml respectant la structure attendue.

        Args:
            fpath (str): Chemin du fichier de configuration `.toml`

        Returns:
            DatashopConfig: Instance configurée selon le fichier renseigné.

        Raises:
            ConfigurationError: Si `strict=True` et que le fichier de configuration n'existe pas!
        """
        fpath = Path(fpath)
        if not fpath.exists():
            raise ConfigurationError(f"Le chemin du fichier de configuration n'existe pas. {fpath=}")

        dico = {}
        try:
            with open(fpath) as fd:
                dico = tomllib.loads(fd.read())

            dico = toml_doc_to_dict(dico)
        except PermissionError:
            msg = f"Accès refusé au chemin {fpath=}"
            raise ConfigurationError(msg)

        if cls.section == 'root':
            return cls(**dico)

        if with_section:
            kwargs = dico.get(cls.section, {})
            if cls.key is None:
                return cls(**kwargs)
            else:
                return cls(**kwargs.get(cls.key, {}))
        else:
            # Flat file without nesting
            if cls.key:
                return cls(**dico.get(cls.key, {}))

    def to_dict(self) -> dict:
        return asdict(self)
