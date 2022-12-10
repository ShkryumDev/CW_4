from dao.model.genre import Genre


class GenreDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, pk):
        return self.session.query(Genre).get(pk)

    def get_all(self, filter):
        page = filter.get('page')

        if page is not None:
            return self.session.query(Genre).paginate(page, per_page=12).items

        return self.session.query(Genre).all()

    def create(self, genre_d):
        ent = Genre(**genre_d)
        self.session.add(ent)
        self.session.commit()
        return ent

    def delete(self, pk):
        genre = self.get_one(pk)
        self.session.delete(genre)
        self.session.commit()

    def update(self, genre_d):
        genre = self.get_one(genre_d.get("id"))
        genre.name = genre_d.get("name")

        self.session.add(genre)
        self.session.commit()
