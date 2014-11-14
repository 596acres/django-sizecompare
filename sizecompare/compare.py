from fractions import Fraction

from .models import SizeComparable


SQFT_PER_ACRE = 43560.0


def _round(factor, digits=1):
    """Round factor to the smallest number of digits possible"""
    rounded = round(factor, digits)
    if rounded:
        return str(rounded)
    return _round(factor, digits + 1)


def _fraction(factor, denominator=10):
    """Get a fraction with a small, understandable denominator"""
    display_fraction = Fraction(str(factor)).limit_denominator(denominator)
    if display_fraction.numerator:
        return str(display_fraction)
    return _fraction(factor, denominator=denominator * 10)


def _smaller(sqft):
    try:
        smaller = SizeComparable.objects.filter(sqft__lte=sqft).order_by('-sqft')[0]
        return {
            'comparable_is': 'smaller',
            'factor': _round(sqft / smaller.sqft),
            'name': smaller.name,
            'sqft': smaller.sqft,
        }
    except Exception:
        return None


def _bigger(sqft):
    try:
        bigger = SizeComparable.objects.filter(sqft__gte=sqft).order_by('sqft')[0]
        bigger_factor = sqft / bigger.sqft
        return {
            'comparable_is': 'bigger',
            'factor': _round(bigger_factor),
            'fraction': _fraction(bigger_factor),
            'name': bigger.name,
            'sqft': bigger.sqft,
        }
    except Exception:
        return None


def find_comparable(sqft=None, acres=None):
    if not sqft:
        try:
            sqft = float(acres) * SQFT_PER_ACRE
        except Exception:
            return dict(success=False)
    else:
        sqft = float(sqft)

    # Gather our choices
    choices = filter(None, [_smaller(sqft), _bigger(sqft)])

    # Sort choices by how close they are to sqft
    choices = sorted(choices, cmp=lambda x, y: int(abs(x['sqft'] - sqft) -
                                                   abs(y['sqft'] - sqft)))

    # Pick one and return it if we have one
    closest = choices[0]
    if closest:
        closest.update({
            'success': True,
        })
    else:
        closest = dict(success=False)
    return closest
