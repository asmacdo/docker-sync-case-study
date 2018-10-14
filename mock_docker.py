import asyncio

from many_many import MockManyMany
from stages import Stage


class Model:
    def __init__(self, num):
        self.abv = None
        self.num = num
        self._saved = False
        self.processed = False
        self._downloaded = False

    @property
    def downloaded(self):
        return self._downloaded

    async def download(self, time=None):
        if time is None:
            time = 1
        await asyncio.sleep(time)
        self._downloaded = True

    @property
    def saved(self):
        return self._saved

    def save(self):
        self._saved = True

    def __repr__(self):
        tab = self.tab * "    "
        proc = "P" if self.processed else "(!p)"
        dl = "D" if self.downloaded else "(!d)"
        save = "S" if self.saved else "(!s)"
        return "{tab}{abv}:{num} {dl}{proc}{save}".format(
            tab=tab, abv=self.abv, num=str(self.num)[0:4], dl=dl, proc=proc, save=save
        )


class Blob(Model):
    def __init__(self, num):
        super().__init__(num)
        self.abv = "B"
        self.processed = True
        self.tab = 2


class Manifest(Blob):
    def __init__(self, num):
        super().__init__(num)
        self.abv = "M"
        self.blobs = []
        self.tab = 1
        self.processed = False

    async def process(self, out_q):
        for i in range(1, 3):  # random.randint(1, 5):
            b_num = self.num + (i / 100)
            b = Blob(b_num)
            self.blobs.append(b)
            await out_q.put(b)
        self.processed = True


class ManifestList(Manifest):
    def __init__(self, num):
        super().__init__(num)
        self.abv = "L"
        self.manifests = []
        self.tab = 0
        self.processed = False

    async def process(self, out_q):
        for i in range(1, 10):  # random.randint(1, 5):
            m_num = self.num + (i / 10)
            m = Manifest(m_num)
            self.manifests.append(m)
            await out_q.put(m)
        self.processed = True


class DockerStart(Stage):
    def __init__(self, blobs=None, manifests=None, manifest_lists=None):
        self.blobs = blobs or 0
        self.manifests = manifests or 0
        self.manifest_lists = manifest_lists or 0

    async def __call__(self, unused_in, out_q):
        for i in range(1, self.manifest_lists + 1):
            ml_num = i
            await out_q.put(ManifestList(ml_num))
        for i in range(1, self.manifests + 1):
            m_num = i / 10
            await out_q.put(Manifest(m_num))
        for i in range(1, self.blobs + 1):
            b_num = i / 100
            await out_q.put(Blob(b_num))
        await out_q.put(None)


class DownloadContent(Stage):
    async def __call__(self, in_q, out_q):
        while True:
            next_in = await in_q.get()
            if next_in is None:
                break
            if next_in.downloaded:
                await out_q.put(next_in)
            else:
                await next_in.download()
                await out_q.put(next_in)
        await out_q.put(None)


class ProcessContent(Stage):
    async def __call__(self, in_q, out_q):
        while True:
            next_in = await in_q.get()
            if next_in is None:
                break
            if next_in.processed or not next_in.downloaded:
                await out_q.put(next_in)
            else:
                await next_in.process(out_q)
                await out_q.put(next_in)
        await out_q.put(None)


class SaveContent(Stage):
    async def __call__(self, in_q, out_q):
        while True:
            next_in = await in_q.get()
            if next_in is None:
                break
            if next_in.saved or not next_in.processed or not next_in.downloaded:
                await out_q.put(next_in)
            else:
                next_in.save()
                await out_q.put(next_in)
        await out_q.put(None)


class ContentRelations(Stage):
    async def __call__(self, in_q, out_q):
        while True:
            next_in = await in_q.get()
            if next_in is None:
                break
            if type(next_in) is ManifestList:
                for manifest in next_in.manifests:
                    MockManyMany.write(next_in, manifest)
            if type(next_in) is Manifest:
                for blob in next_in.blobs:
                    MockManyMany.write(next_in, blob)
            if type(next_in) is Blob:
                pass
            await out_q.put(next_in)
        await out_q.put(None)
