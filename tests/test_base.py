from fake_openerp import monkey_patch
monkey_patch()

from osv.osv import get_object


class TestPartner(object):
    @classmethod
    def setup(cls):
        cls.p = get_object('res_partner')

    def test_partner_validate_cpf(self):
        # it shouldnt accept invalid cpf
        assert not self.p.validate_cpf('932')
        assert not self.p.validate_cpf('887.687.331-77')
        # it should accept valid cpf numbers
        assert self.p.validate_cpf('887.687.331-78')
        assert self.p.validate_cpf('64785949120')
        assert self.p.validate_cpf('58790082583')
