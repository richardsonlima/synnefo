# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from synnefo.db.models import BridgePool

class Migration(DataMigration):
    
    def forwards(self, orm):
        "Write your forwards methods here."
        for network in orm.Network.objects.all():
            if network.state == 'DELETED':
                network.deleted = True

            if network.public == True:
                # Public Network
                network.netlink = network.link.name
                network.dhcp = True
                network.type = 'PUBLIC_ROUTED'
            else:
                network.dhcp = False
                network.type = 'PRIVATE_VLAN'
                bridge = BridgePool.get_available()
                network.netlink = bridge.value

            network.save()
    
    
    def backwards(self, orm):
        "Write your backwards methods here."
        pass
    
    models = {
        'db.backend': {
            'Meta': {'object_name': 'Backend'},
            'clustername': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'ctotal': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'dfree': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'drained': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'dtotal': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'hash': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mfree': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'mtotal': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'offline': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'pinst_cnt': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'port': ('django.db.models.fields.PositiveIntegerField', [], {'default': '5080'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'})
        },
        'db.bridgepool': {
            'Meta': {'object_name': 'BridgePool'},
            'available': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        'db.flavor': {
            'Meta': {'unique_together': "(('cpu', 'ram', 'disk', 'disk_template'),)", 'object_name': 'Flavor'},
            'cpu': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'disk': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'disk_template': ('django.db.models.fields.CharField', [], {'default': "'drbd'", 'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ram': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'db.macprefixpool': {
            'Meta': {'object_name': 'MacPrefixPool'},
            'available': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        'db.network': {
            'Meta': {'object_name': 'Network'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'backendjobid': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'backendjobstatus': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'backendlogmsg': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'backendopcode': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'backendtime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(1, 1, 1, 0, 0)'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'dhcp': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'gateway': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['db.NetworkLink']"}),
            'mac_prefix': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'machines': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['db.VirtualMachine']", 'through': "orm['db.NetworkInterface']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'netlink': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'PENDING'", 'max_length': '30'}),
            'subnet': ('django.db.models.fields.CharField', [], {'default': "'10.0.0.0/24'", 'max_length': '32'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'PRIVATE_VLAN'", 'max_length': '50'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'userid': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'})
        },
        'db.networkinterface': {
            'Meta': {'object_name': 'NetworkInterface'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'firewall_profile': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'ipv4': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'ipv6': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'mac': ('django.db.models.fields.CharField', [], {'max_length': '17', 'null': 'True'}),
            'machine': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nics'", 'to': "orm['db.VirtualMachine']"}),
            'network': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nics'", 'to': "orm['db.Network']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'db.networklink': {
            'Meta': {'object_name': 'NetworkLink'},
            'available': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'network': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['db.Network']"})
        },
        'db.virtualmachine': {
            'Meta': {'object_name': 'VirtualMachine'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'backend': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'virtual_machines'", 'null': 'True', 'to': "orm['db.Backend']"}),
            'backend_hash': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'backendjobid': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'backendjobstatus': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'backendlogmsg': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'backendopcode': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'backendtime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(1, 1, 1, 0, 0)'}),
            'buildpercentage': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'flavor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['db.Flavor']"}),
            'hostid': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imageid': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'operstate': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'suspended': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'userid': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'db.virtualmachinemetadata': {
            'Meta': {'unique_together': "(('meta_key', 'vm'),)", 'object_name': 'VirtualMachineMetadata'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta_key': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'meta_value': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'vm': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'metadata'", 'to': "orm['db.VirtualMachine']"})
        }
    }
    
    complete_apps = ['db']
