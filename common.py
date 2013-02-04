class RichEqualityMixin(object):
	def __eq__(self, other):
		raise NotImplementedError("Equality not implemented")

	def __lt__(self, other):
		raise NotImplementedError("Less than not implemented")

	def __ne__(self, other):
		return not self.__eq__(other)

	def __gt__(self, other):
		return not (self.__lt__(other) or self.__eq__(other))

	def __le__(self, other):
		return self.__eq__(other) or self.__lt__(other)

	def __ge__(self, other):
		return self.__eq__(other) or self.__gt__(other)

class CommonEqualityMixin(RichEqualityMixin):

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and self.__dict__ == other.__dict__)
