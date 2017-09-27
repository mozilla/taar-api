import json
from django.core.management.base import BaseCommand
from django.conf import settings
from happybase.connection import Connection


class Command(BaseCommand):
    help = 'Populate the HBase table with some sample data'

    def handle(self, *args, **options):
        conn = Connection(settings.HBASE_HOST)
        if settings.HBASE_TABLE.encode() not in conn.tables():
            self.stderr.write(
                self.style.ERROR('Table "%s" not found.' % settings.HBASE_TABLE))
        table = conn.table(settings.HBASE_TABLE)
        data = json.dumps({
                'active_addons': [
                    {
                        'addon_id': '_jvMembers_@free.notehomepage.com',
                        'app_disabled': False,
                        'blocklisted': False,
                        'foreign_install': False,
                        'has_binary_components': False,
                        'install_day': 17366,
                        'is_system': False,
                        'is_web_extension': False,
                        'name': 'NoteHomepage',
                        'scope': 1,
                        'signed_state': 2,
                        'type': 'extension',
                        'update_day': 17368,
                        'user_disabled': False,
                        'version': '7.800.11.22073'
                    },
                    {
                        'addon_id': 'firefox@getpocket.com',
                        'app_disabled': False,
                        'blocklisted': False,
                        'foreign_install': False,
                        'has_binary_components': False,
                        'install_day': 17345,
                        'is_system': True,
                        'is_web_extension': False,
                        'name': 'Pocket',
                        'scope': 1,
                        'type': 'extension',
                        'update_day': 17345,
                        'user_disabled': False,
                        'version': '1.0.5'
                    }
                ],
                'active_addons_count': 10,
                'active_theme': {
                    'addon_id': '{972ce4c6-7e08-4474-a285-3208198ce6fd}',
                    'app_disabled': False,
                    'blocklisted': False,
                    'foreign_install': False,
                    'has_binary_components': False,
                    'install_day': 17345,
                    'name': 'Default',
                    'scope': 4,
                    'update_day': 17345,
                    'user_disabled': False,
                    'version': '54.0.1'
                },
                'active_ticks': 87,
                'addon_compatibility_check_enabled': True,
                'app_build_id': '20170628075643',
                'app_display_version': '54.0.1',
                'app_name': 'Firefox',
                'app_version': '54.0.1',
                'attribution': {
                    'campaign': '%2528not%2Bset%2529',
                    'content': '%2528not%2Bset%2529',
                    'medium': 'referral',
                    'source': 'www.google.dz'
                },
                'blocklist_enabled': True,
                'channel': 'release',
                'city': '??',
                'client_submission_date': 'Sat, 22 Jul 2017 04:10:27 GMT',
                'country': 'DZ',
                'creation_date': '2017-07-22T04:10:27.601Z',
                'default_search_engine': 'google',
                'default_search_engine_data_load_path': 'jar:[app]/omni.ja!browser/google.xml',
                'default_search_engine_data_name': 'Google',
                'default_search_engine_data_origin': 'default',
                'e10s_cohort': 'disqualified-test',
                'e10s_enabled': False,
                'env_build_arch': 'x86',
                'env_build_id': '20170628075643',
                'env_build_version': '54.0.1',
                'first_paint': 3779,
                'install_year': 2017,
                'is_default_browser': True,
                'is_wow64': False,
                'locale': 'en-US',
                'main': 175,
                'memory_mb': 2972,
                'normalized_channel': 'release',
                'os': 'Windows_NT',
                'os_service_pack_major': 0,
                'os_service_pack_minor': 0,
                'os_version': '6.1',
                'profile_creation_date': 17360,
                'profile_subsession_counter': 129,
                'quantum_ready': False,
                'reason': 'environment-change',
                'sample_id': '50',
                'session_restored': 4646,
                'ssl_handshake_result': {'0': 81},
                'ssl_handshake_result_failure': 0,
                'ssl_handshake_result_success': 81,
                'submission_date': '20170722',
                'subsession_counter': 1,
                'subsession_length': 544,
                'subsession_start_date': '2017-07-22T00:00:00.0+02:00',
                'sync_configured': True,
                'sync_count_desktop': 1,
                'sync_count_mobile': 0,
                'telemetry_enabled': True,
                'timestamp': 1500700236140496896,
                'timezone_offset': 120,
                'total_time': 547,
                'vendor': 'Mozilla',
                'windows_build_number': 7600
            })
        client_id = "299f6da0-6f97-48a0-a1f3-6f836c46ce0c"
        table.put("%s" % client_id, {b'cf:payload': data.encode()})
