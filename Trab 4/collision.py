
def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


@singleton
class Collider:

    def colidiu(self, o1, o2):
        offset = (
            int(o2.x - o1.x),
            int(o2.y - o1.y)
        )

        return o1.mask.overlap(o2.mask, offset) is not None

    def refletir(self, pato, obstaculo):
       
        pato.vy = -abs(pato.vy) - 2

    def pontuar(self, pato, bonus):
        pato.pontos += 10
