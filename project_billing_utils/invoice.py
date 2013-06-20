# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2010 Camptocamp SA (http://www.camptocamp.com)
# All Right Reserved
#
# Author : Joel Grand-guillaume (Camptocamp)
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

from osv import osv, fields
from tools.translate import _

class AccountInvoice(osv.osv):
    _inherit = 'account.invoice'

    def name_get(self, cr, uid, ids, context=None):
        if not context.has_key('special_search'):
            return super(AccountInvoice,self).name_get(cr, uid, ids, context=context)
        else:
            if not ids:
                return []
            ## We will return value  
            rest = []
            for r in self.read(cr,uid,ids, ['number','partner_id','name'], context):
                rest.append((r['id'],('%s - %s - %s'%(r['number'] or '',r['partner_id'][1],r['name'] or '') )))
                              
                ## We will 
            return rest

    def name_search(self, cr, user, name, args=None, operator='ilike', context=None, limit=100):
        if not context.has_key('special_search'):
            return super(AccountInvoice,self).name_search(cr, user, name, args=args, operator=operator, context=context, limit=limit)
        if not args:
            args = []
        if context is None:
            context = {}
        ids = []
        if name:
            ids = self.search(cr, user, [('number',operator,name)] + args, limit=limit, context=context)
        if not ids:
            ids = self.search(cr, user, [('commercial_partner_id.name',operator,name)] + args, limit=limit, context=context)
        if not ids:
            ids = self.search(cr, user, [('partner_id.name',operator,name)] + args, limit=limit, context=context)
        return self.name_get(cr, user, ids, context)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: