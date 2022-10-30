import json
import keyword


class DynamicAttributes:
    def __init__(self, attributes):
        for attr, value in attributes.items():
            if keyword.iskeyword(attr):
                attr = attr + '_'
            if isinstance(value, dict):
                setattr(self, attr, DynamicAttributes(value))
            else:
                setattr(self, attr, value)


class ColorizeMixin:
    def __repr__(self):
        return f'\033[1;{self.repr_color_code};40m {self.title} | {self.price} ₽'


class Advert(ColorizeMixin, DynamicAttributes):
    repr_color_code = 33

    def set_default_price(self):
        try:
            getattr(self, 'price')
        except AttributeError:
            setattr(self, 'price', 0)

        if getattr(self, 'price') < 0:
            raise ValueError('must be >= 0')

    def __init__(self, data):
        if isinstance(data, dict):
            json_data_to_python = data
        else:
            json_data_to_python = json.loads(data)

        super().__init__(json_data_to_python)
        getattr(self, 'title')
        self.set_default_price()

    def __repr__(self):
        if issubclass(Advert, ColorizeMixin):
            return ColorizeMixin.__repr__(self)
        else:
            return f'{self.title} | {self.price} ₽'


if __name__ == '__main__':
    example_1 = '{"title": "iPhone X","price": 100, "location": {"address": "город Самара, улица Мориса Тореза, 50","metro_stations": ["Спортивная", "Гагаринская"]}}'
    example_2 = '{"title": "Вельш-корги","price": 1000,"class": "dogs","location": {"address": "сельское поселение Ельдигинское, поселок санатория Тишково, 25"}}'
    # example_1_negative_price = '{"title": "iPhone X","price": -20, "location": {"address": "город Самара, улица Мориса Тореза, 50","metro_stations": ["Спортивная", "Гагаринская"]}}'

    iphone_ad = Advert(example_1)
    corgi = Advert(example_2)

    # iphone_ad_negative_price = Advert(example_1_negative_price)

    print(iphone_ad.location.address)
    print(corgi.class_)
