from flask import Blueprint, request, jsonify
from models import db, Song, Setlist
import pandas as pd
import random
import io
from datetime import datetime

# Create a Blueprint for API routes
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Song routes
@api_bp.route('/songs', methods=['GET'])
def get_songs():
    songs = Song.query.all()
    return jsonify([song.to_dict() for song in songs])

@api_bp.route('/songs/<int:song_id>', methods=['GET'])
def get_song(song_id):
    song = Song.query.get_or_404(song_id)
    return jsonify(song.to_dict())

@api_bp.route('/songs', methods=['POST'])
def create_song():
    data = request.json
    
    # Create new song from request data
    new_song = Song(
        title=data['title'],
        artist=data['artist'],
        tempo=data.get('tempo'),
        tempo_category=data.get('tempo_category'),
        intensity=data.get('intensity'),
        lead_vocalist=data.get('lead_vocalist'),
        key=data.get('key'),
        is_minor=data.get('is_minor', False),
        is_original=data.get('is_original', True),
        is_hit=data.get('is_hit', False),
        duration=data.get('duration')
    )
    
    db.session.add(new_song)
    db.session.commit()
    
    return jsonify(new_song.to_dict()), 201

@api_bp.route('/songs/<int:song_id>', methods=['PUT'])
def update_song(song_id):
    song = Song.query.get_or_404(song_id)
    data = request.json
    
    # Update song fields
    song.title = data.get('title', song.title)
    song.artist = data.get('artist', song.artist)
    song.tempo = data.get('tempo', song.tempo)
    song.tempo_category = data.get('tempo_category', song.tempo_category)
    song.intensity = data.get('intensity', song.intensity)
    song.lead_vocalist = data.get('lead_vocalist', song.lead_vocalist)
    song.key = data.get('key', song.key)
    song.is_minor = data.get('is_minor', song.is_minor)
    song.is_original = data.get('is_original', song.is_original)
    song.is_hit = data.get('is_hit', song.is_hit)
    song.duration = data.get('duration', song.duration)
    
    db.session.commit()
    
    return jsonify(song.to_dict())

@api_bp.route('/songs/<int:song_id>', methods=['DELETE'])
def delete_song(song_id):
    song = Song.query.get_or_404(song_id)
    db.session.delete(song)
    db.session.commit()
    
    return jsonify({'message': 'Song deleted successfully'})

# CSV Upload route
@api_bp.route('/songs/upload', methods=['POST'])
def upload_songs():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and file.filename.endswith('.csv'):
        # Read CSV file
        csv_data = pd.read_csv(file)
        
        # Process each row in the CSV
        songs_added = 0
        for _, row in csv_data.iterrows():
            # Check if required fields exist
            if 'title' not in row or 'artist' not in row:
                continue
                
            # Create new song from CSV data
            new_song = Song(
                title=row['title'],
                artist=row['artist'],
                tempo=row.get('tempo'),
                tempo_category=row.get('tempo_category'),
                intensity=row.get('intensity'),
                lead_vocalist=row.get('lead_vocalist'),
                key=row.get('key'),
                is_minor=row.get('is_minor', False) if 'is_minor' in row else None,
                is_original=row.get('is_original', True) if 'is_original' in row else None,
                is_hit=row.get('is_hit', False) if 'is_hit' in row else None,
                duration=row.get('duration')
            )
            
            db.session.add(new_song)
            songs_added += 1
        
        db.session.commit()
        
        return jsonify({'message': f'{songs_added} songs added successfully'})
    
    return jsonify({'error': 'Invalid file format'}), 400

# Setlist routes
@api_bp.route('/setlists', methods=['GET'])
def get_setlists():
    setlists = Setlist.query.all()
    return jsonify([setlist.to_dict() for setlist in setlists])

@api_bp.route('/setlists/<int:setlist_id>', methods=['GET'])
def get_setlist(setlist_id):
    setlist = Setlist.query.get_or_404(setlist_id)
    return jsonify(setlist.to_dict())

@api_bp.route('/setlists', methods=['POST'])
def create_setlist():
    data = request.json
    
    # Create new setlist
    new_setlist = Setlist(
        name=data['name'],
        date=datetime.strptime(data['date'], '%Y-%m-%d').date() if 'date' in data else None,
        venue=data.get('venue'),
        total_duration=data.get('total_duration')
    )
    
    # Add songs to setlist if provided
    if 'song_ids' in data:
        for song_id in data['song_ids']:
            song = Song.query.get(song_id)
            if song:
                new_setlist.songs.append(song)
    
    db.session.add(new_setlist)
    db.session.commit()
    
    return jsonify(new_setlist.to_dict()), 201

@api_bp.route('/setlists/<int:setlist_id>', methods=['DELETE'])
def delete_setlist(setlist_id):
    setlist = Setlist.query.get_or_404(setlist_id)
    db.session.delete(setlist)
    db.session.commit()
    
    return jsonify({'message': 'Setlist deleted successfully'})

# Setlist generation route
@api_bp.route('/generate-setlist', methods=['POST'])
def generate_setlist():
    data = request.json
    
    # Get parameters for setlist generation
    target_duration = data.get('target_duration', 3600)  # Default to 1 hour in seconds
    name = data.get('name', f'Setlist {datetime.now().strftime("%Y-%m-%d")}')
    date = data.get('date')
    venue = data.get('venue')
    
    # Get all songs from the database
    all_songs = Song.query.all()
    
    if not all_songs:
        return jsonify({'error': 'No songs in the database'}), 400
    
    # First, include all hit songs
    hit_songs = [song for song in all_songs if song.is_hit]
    random.shuffle(hit_songs)
    
    # Calculate remaining duration after including hit songs
    hit_songs_duration = sum(song.duration or 0 for song in hit_songs)
    remaining_duration = target_duration - hit_songs_duration
    
    # Filter out hit songs from the pool of available songs and shuffle to break
    # any inherent ordering from the database
    available_songs = [song for song in all_songs if not song.is_hit]
    random.shuffle(available_songs)
    
    # Group songs by their attributes for balanced distribution
    songs_by_key_type = {'major': [], 'minor': []}
    songs_by_tempo = {'slow': [], 'medium': [], 'fast': []}
    songs_by_type = {'original': [], 'cover': []}
    songs_by_vocalist = {}
    
    # Helper function to normalize tempo category
    def normalize_tempo_category(category):
        if not category:
            return None
        category = category.lower()
        if category in ['slow', 'medium', 'fast']:
            return category
        elif category in ['s', 'sl', 'slo']:
            return 'slow'
        elif category in ['m', 'med', 'mid']:
            return 'medium'
        elif category in ['f', 'fa', 'fas']:
            return 'fast'
        return None
    
    for song in available_songs:
        # Group by key type
        key_type = 'minor' if song.is_minor else 'major'
        songs_by_key_type[key_type].append(song)
        
        # Group by tempo - normalize the category first
        if song.tempo_category:
            normalized_category = normalize_tempo_category(song.tempo_category)
            if normalized_category:
                songs_by_tempo[normalized_category].append(song)
        
        # Group by song type
        song_type = 'original' if song.is_original else 'cover'
        songs_by_type[song_type].append(song)
        
        # Group by vocalist
        if song.lead_vocalist:
            if song.lead_vocalist not in songs_by_vocalist:
                songs_by_vocalist[song.lead_vocalist] = []
            songs_by_vocalist[song.lead_vocalist].append(song)
    
    # Initialize the setlist with hit songs
    setlist_songs = hit_songs.copy()
    
    # Function to get the next song that balances the setlist
    def get_next_song(current_setlist, remaining_songs):
        if not remaining_songs:
            return None

        # Filter out songs that would violate sequencing rules:
        # 1) No more than two originals in a row
        # 2) No two slow songs in a row
        # 3) No more than two minor songs in a row
        # 4) No more than two fast songs in a row
        # 5) No more than two songs from the same vocalist in a row
        def violates_rules(candidate):
            if len(current_setlist) >= 2:
                if (current_setlist[-1].is_original and
                        current_setlist[-2].is_original and
                        candidate.is_original):
                    return True
                if (current_setlist[-1].is_minor and
                        current_setlist[-2].is_minor and
                        candidate.is_minor):
                    return True
                last_fast = normalize_tempo_category(current_setlist[-1].tempo_category) == 'fast'
                prev_fast = normalize_tempo_category(current_setlist[-2].tempo_category) == 'fast'
                cand_fast = normalize_tempo_category(candidate.tempo_category) == 'fast'
                if last_fast and prev_fast and cand_fast:
                    return True
                last_vocal = current_setlist[-1].lead_vocalist
                prev_vocal = current_setlist[-2].lead_vocalist
                cand_vocal = candidate.lead_vocalist
                if last_vocal and prev_vocal and cand_vocal and last_vocal == prev_vocal == cand_vocal:
                    return True
            if len(current_setlist) >= 1:
                last_tempo = normalize_tempo_category(current_setlist[-1].tempo_category)
                cand_tempo = normalize_tempo_category(candidate.tempo_category)
                if last_tempo == 'slow' and cand_tempo == 'slow':
                    return True
            return False

        valid_songs = [s for s in remaining_songs if not violates_rules(s)]
        if not valid_songs:
            valid_songs = remaining_songs
            
        # Count current distribution
        key_counts = {'major': 0, 'minor': 0}
        tempo_counts = {'slow': 0, 'medium': 0, 'fast': 0}
        type_counts = {'original': 0, 'cover': 0}
        vocalist_counts = {}
        
        for song in current_setlist:
            # Count key types
            key_type = 'minor' if song.is_minor else 'major'
            key_counts[key_type] += 1
            
            # Count tempos - use the same normalization function
            if song.tempo_category:
                normalized_category = normalize_tempo_category(song.tempo_category)
                if normalized_category:
                    tempo_counts[normalized_category] += 1
            
            # Count song types
            song_type = 'original' if song.is_original else 'cover'
            type_counts[song_type] += 1
            
            # Count vocalists
            if song.lead_vocalist:
                if song.lead_vocalist not in vocalist_counts:
                    vocalist_counts[song.lead_vocalist] = 0
                vocalist_counts[song.lead_vocalist] += 1
        
        # Find the most underrepresented categories
        min_key_type = min(key_counts, key=lambda k: key_counts[k])
        min_tempo = min(tempo_counts, key=lambda t: tempo_counts[t])
        min_song_type = min(type_counts, key=lambda t: type_counts[t])
        
        # Find the vocalist with the least songs
        min_vocalist = None
        if vocalist_counts:
            min_vocalist = min(vocalist_counts, key=lambda v: vocalist_counts[v])
        
        # Score each remaining song based on how well it balances the setlist
        scored_songs = []
        for song in valid_songs:
            score = 0
            
            # Score for key type
            song_key_type = 'minor' if song.is_minor else 'major'
            if song_key_type == min_key_type:
                score += 1
            
            # Score for tempo
            normalized_category = normalize_tempo_category(song.tempo_category) if song.tempo_category else None
            if normalized_category and normalized_category == min_tempo:
                score += 1
            
            # Score for song type
            song_type = 'original' if song.is_original else 'cover'
            if song_type == min_song_type:
                score += 1
            
            # Score for vocalist
            if min_vocalist and song.lead_vocalist == min_vocalist:
                score += 1
            
            scored_songs.append((song, score))
        
        if not scored_songs:
            return None

        # Introduce randomness while favoring higher scores
        songs, scores = zip(*scored_songs)
        # Use score + 1 to ensure non-zero weight for all songs
        weights = [s + 1 for s in scores]
        return random.choices(songs, weights=weights, k=1)[0]
    
    # Build the setlist by adding songs that balance it
    while remaining_duration > 0 and available_songs:
        next_song = get_next_song(setlist_songs, available_songs)
        
        if not next_song:
            break
            
        # Add song to setlist and remove from available pool
        if next_song.duration and next_song.duration <= remaining_duration:
            setlist_songs.append(next_song)
            available_songs.remove(next_song)
            remaining_duration -= next_song.duration
        else:
            # If song is too long, remove it from consideration
            available_songs.remove(next_song)

    def sequence_valid(songs):
        """Check sequencing rules for a list of songs."""
        originals_in_row = 0
        minors_in_row = 0
        fast_in_row = 0
        last_tempo = None
        last_vocals = []
        for s in songs:
            # Original rule
            if s.is_original:
                originals_in_row += 1
            else:
                originals_in_row = 0
            if originals_in_row > 2:
                return False

            # Minor rule
            if s.is_minor:
                minors_in_row += 1
            else:
                minors_in_row = 0
            if minors_in_row > 2:
                return False

            # Tempo rules
            tempo = normalize_tempo_category(s.tempo_category) if s.tempo_category else None
            if tempo == 'fast':
                fast_in_row += 1
            else:
                fast_in_row = 0
            if fast_in_row > 2:
                return False
            if last_tempo == 'slow' and tempo == 'slow':
                return False
            last_tempo = tempo

            # Vocalist rule
            last_vocals.append(s.lead_vocalist)
            if len(last_vocals) > 3:
                last_vocals = last_vocals[-3:]
            if len(last_vocals) == 3 and last_vocals[0] and last_vocals[0] == last_vocals[1] == last_vocals[2]:
                return False

        return True

    def halves_balanced(songs):
        """Ensure the second half roughly matches the first half for key, tempo and type."""
        if not songs:
            return True
        mid = len(songs) // 2
        first = songs[:mid]
        second = songs[mid:]

        def count(lst, func):
            return sum(1 for s in lst if func(s))

        checks = []
        checks.append(abs(count(first, lambda s: s.is_original) - count(second, lambda s: s.is_original)) <= 1)
        checks.append(abs(count(first, lambda s: s.is_minor) - count(second, lambda s: s.is_minor)) <= 1)
        checks.append(abs(count(first, lambda s: normalize_tempo_category(s.tempo_category) == 'slow') -
                        count(second, lambda s: normalize_tempo_category(s.tempo_category) == 'slow')) <= 1)
        checks.append(abs(count(first, lambda s: normalize_tempo_category(s.tempo_category) == 'fast') -
                        count(second, lambda s: normalize_tempo_category(s.tempo_category) == 'fast')) <= 1)
        return all(checks)

    def shuffle_setlist_order(songs, attempts=1000):
        """Randomize order while keeping sequencing rules and half balance."""
        songs = songs.copy()
        # Try a number of full shuffles first
        for _ in range(attempts):
            random.shuffle(songs)
            if sequence_valid(songs) and halves_balanced(songs):
                return songs

        # If no perfect shuffle found, build the order greedily while checking
        # the rules. This fallback helps avoid returning an invalid sequence.
        remaining = songs.copy()
        random.shuffle(remaining)
        ordered = []
        while remaining:
            candidates = [s for s in remaining if sequence_valid(ordered + [s])]
            if not candidates:
                break
            next_song = random.choice(candidates)
            ordered.append(next_song)
            remaining.remove(next_song)

        if ordered and sequence_valid(ordered) and halves_balanced(ordered):
            return ordered
        return songs

    # Randomize final order while respecting sequencing rules
    setlist_songs = shuffle_setlist_order(setlist_songs)

    # Create the setlist in the database
    new_setlist = Setlist(
        name=name,
        date=datetime.strptime(date, '%Y-%m-%d').date() if date else None,
        venue=venue,
        total_duration=target_duration - remaining_duration
    )
    
    # Add songs to the setlist
    for song in setlist_songs:
        new_setlist.songs.append(song)
    
    db.session.add(new_setlist)
    db.session.commit()
    
    return jsonify(new_setlist.to_dict()), 201
