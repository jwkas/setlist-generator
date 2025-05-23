import unittest
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from app import create_app
from models import db, Song
from config import Config

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True
    DEBUG = False

class SetlistRulesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            # Add sample songs
            songs = [
                Song(title='Slow Original 1', artist='Band', tempo=70, tempo_category='slow', is_original=True, is_minor=False, lead_vocalist='A', duration=200),
                Song(title='Slow Original 2', artist='Band', tempo=72, tempo_category='slow', is_original=True, is_minor=True, lead_vocalist='B', duration=200),
                Song(title='Slow Cover', artist='Band', tempo=68, tempo_category='slow', is_original=False, is_minor=True, lead_vocalist='A', duration=200),
                Song(title='Fast Original', artist='Band', tempo=120, tempo_category='fast', is_original=True, is_minor=False, lead_vocalist='C', duration=200),
                Song(title='Medium Cover', artist='Band', tempo=100, tempo_category='medium', is_original=False, is_minor=False, lead_vocalist='A', duration=200),
                Song(title='Fast Cover', artist='Band', tempo=130, tempo_category='fast', is_original=False, is_minor=True, lead_vocalist='B', duration=200),
                Song(title='Medium Original', artist='Band', tempo=110, tempo_category='medium', is_original=True, is_minor=False, lead_vocalist='C', duration=200),
                Song(title='Fast Major Cover', artist='Band', tempo=125, tempo_category='fast', is_original=False, is_minor=False, lead_vocalist='A', duration=200),
            ]
            db.session.add_all(songs)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_setlist_generation_rules(self):
        payload = {'target_duration': 1200, 'name': 'Test Set'}
        response = self.client.post('/api/generate-setlist', json=payload)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        titles = [s['title'] for s in data['songs']]
        originals_in_a_row = 0
        minors_in_a_row = 0
        fast_in_a_row = 0
        last_tempo = None
        last_vocals = []
        for song in data['songs']:
            if song['is_original']:
                originals_in_a_row += 1
            else:
                originals_in_a_row = 0
            self.assertLessEqual(originals_in_a_row, 2)

            if song['is_minor']:
                minors_in_a_row += 1
            else:
                minors_in_a_row = 0
            self.assertLessEqual(minors_in_a_row, 2)

            tempo = song['tempo_category']
            if tempo:
                tempo = tempo.lower()
            if tempo == 'fast':
                fast_in_a_row += 1
            else:
                fast_in_a_row = 0
            self.assertLessEqual(fast_in_a_row, 2)
            if last_tempo == 'slow' and tempo == 'slow':
                self.fail('Two slow songs in a row found')
            last_tempo = tempo

            last_vocals.append(song['lead_vocalist'])
            if len(last_vocals) > 3:
                last_vocals = last_vocals[-3:]
            if len(last_vocals) == 3 and last_vocals[0] and last_vocals[0] == last_vocals[1] == last_vocals[2]:
                self.fail('More than two songs from the same vocalist in a row')

        # Check half balance
        mid = len(data['songs']) // 2
        first = data['songs'][:mid]
        second = data['songs'][mid:]

        def count(lst, predicate):
            return sum(1 for s in lst if predicate(s))

        self.assertLessEqual(abs(count(first, lambda s: s['is_original']) - count(second, lambda s: s['is_original'])), 1)
        self.assertLessEqual(abs(count(first, lambda s: s['is_minor']) - count(second, lambda s: s['is_minor'])), 1)
        self.assertLessEqual(abs(count(first, lambda s: s['tempo_category'] and s['tempo_category'].lower() == 'slow') -
                              count(second, lambda s: s['tempo_category'] and s['tempo_category'].lower() == 'slow')), 1)
        self.assertLessEqual(abs(count(first, lambda s: s['tempo_category'] and s['tempo_category'].lower() == 'fast') -
                              count(second, lambda s: s['tempo_category'] and s['tempo_category'].lower() == 'fast')), 1)

if __name__ == '__main__':
    unittest.main()
