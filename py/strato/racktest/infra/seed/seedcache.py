import logging
import time
from strato.racktest.infra.seed import seedcreator


class SeedCache:
    def __init__(self, engine):
        self._engine = engine

    def make(self, key, code, takeSitePackages=False, excludePackages=None, joinPythonNamespaces=True,
             callableRootPath=None):
        with self._engine.lock(key):
            seed = self._engine.get(key)
            if seed is not None:
                logging.debug('Cache hit for key %(key)s', dict(key=key))
                return seed
            logging.debug('Cache miss for %(key)s', dict(key=key))
            before = time.time()
            creator = seedcreator.SeedCreator(code,
                                              generateDependencies=True,
                                              takeSitePackages=takeSitePackages,
                                              excludePackages=excludePackages,
                                              joinPythonNamespaces=joinPythonNamespaces,
                                              callableRootPath=callableRootPath)
            seed = creator.create()
            after = time.time()
            self._engine.install(key, seed)
            logging.debug('Seed generation took %(delta).3f sec', dict(delta=after - before))
            return seed
