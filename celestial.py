import horizons

positions = horizons.getstars()

signs = {
    330 : "Pisces",
    300 : "Aquarius",
    270 : "Capricorn",
    240 : "Sagittarius",
    210 : "Scorpio",
    180 : "Libra",
    150 : "Virgo",
    120 : "Leo",
    90  : "Cancer",
    60  : "Gemini",
    30  : "Taurus",
    0   : "Aries"
}

class Celestial:
    def __init__(self, name, absolute):
        self.name = name
        self.absolute = absolute
        for sign in signs:
            if absolute > float(sign):
                self.sign = signs[sign]
    def __repr__(self):
        return "{} - ObsEcLon {}°".format(self.name, self.absolute)

celestials = {}
for star in positions:
    celestials[star] = Celestial(star, positions[star])

print(celestials)
