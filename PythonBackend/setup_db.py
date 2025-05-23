import sqlite3

def create_tables():
    conn = sqlite3.connect("chameleo.db")
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        username TEXT PRIMARY KEY
    )""")
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Videos (
            video_id INTEGER PRIMARY KEY,
            title TEXT,
            file_path TEXT,
            tags TEXT
        )""")
        
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS UserVideoInteraction (
            username TEXT REFERENCES Users(username),
            video_id INTEGER REFERENCES Videos(video_id),
            watch_percentage FLOAT,
            PRIMARY KEY (username, video_id)
        )""")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS VideoSimilarity (
            video1_id INTEGER REFERENCES Videos(video_id),
            video2_id INTEGER REFERENCES Videos(video_id),
            similarity FLOAT,
            PRIMARY KEY (video1_id, video2_id)
        )""")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Clusters (
            cluster_id INTEGER,
            video_id INTEGER REFERENCES Videos(video_id),
            PRIMARY KEY (cluster_id, video_id)
        )""")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS UserPreferences (
            username TEXT REFERENCES Users(username),
            cluster_id INTEGER REFERENCES Clusters(cluster_id), -- Matches Leiden cluster ID format
            opted_out BOOLEAN,
            PRIMARY KEY (username, cluster_id)
        )""")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Recommendations (
            username TEXT REFERENCES Users(username),
            video_id INTEGER REFERENCES Videos(video_id),
            rsef_score FLOAT,
            PRIMARY KEY (username, video_id)
        )""")

    conn.commit()
    conn.close()

def insert_sample_data():
    conn = sqlite3.connect("chameleo.db")
    cursor = conn.cursor()
    
    users = [("user1"), ("user2"), ("user3"), ("user4"), ("user5"), ("user6"), ("user7"), ("user8"), ("user9"), ("user10"), ("user11"), ("user12"), ("user13"), ("user14"), ("user15")]
    cursor.executemany("INSERT OR IGNORE INTO Users (username) VALUES (?)", [(u,) for u in users])
    
    videos = [
        (0, 'Dog and cat memes', '/home/favas/chameleo_app/assets/VideoData/video_001.mp4', 'funny,cat,dog,animals,memes,comedy'),
        (1, 'Funny pet videos', '/home/favas/chameleo_app/assets/VideoData/video_002.mp4', 'funny,cat,dog,animals,memes,comedy'),
        (2, 'Indian Standup comedy', '/home/favas/chameleo_app/assets/VideoData/video_003.mp4', 'standup,comedy'),
        (3, '3 minute intense workout', '/home/favas/chameleo_app/assets/VideoData/video_101.mp4', 'workout,gym,exercise,fitness,health'),
        (4, '5 Common Food Myths', '/home/favas/chameleo_app/assets/VideoData/video_102.mp4', 'food,health'),
        (5, '5-minute meditation you can do anywhere', '/home/favas/chameleo_app/assets/VideoData/video_103.mp4', 'health,exercise,meditation'),
        (6, 'Best strength training exercises', '/home/favas/chameleo_app/assets/VideoData/video_104.mp4', 'workout,gym,exercise,fitness,health'),
        (7, 'Calisthenics wrist stretching', '/home/favas/chameleo_app/assets/VideoData/video_105.mp4', 'workout,gym,exercise,fitness,health'),
        (8, 'Cardio tips', '/home/favas/chameleo_app/assets/VideoData/video_106.mp4', 'workout,gym,exercise,fitness,health'),
        (9, 'Easy protein rich breakfast', '/home/favas/chameleo_app/assets/VideoData/video_107.mp4', 'food,recipe,health'),
        (10, 'Gym memes', '/home/favas/chameleo_app/assets/VideoData/video_108.mp4', 'workout,gym,exercise,fitness,health,comedy,memes'),
        (11, 'Protein shake recipes', '/home/favas/chameleo_app/assets/VideoData/video_109.mp4', 'food,recipe,health'),
        (12, 'Yoga for beginner', '/home/favas/chameleo_app/assets/VideoData/video_110.mp4', 'health,exercise,meditation'),
        (13, 'Bgmi highlights', '/home/favas/chameleo_app/assets/VideoData/video_201.mp4', 'gaming,highlights'),
        (14, 'Clash of clans TH17 strategy', '/home/favas/chameleo_app/assets/VideoData/video_202.mp4', 'gaming,strategy'),
        (15, 'eFootball best goals', '/home/favas/chameleo_app/assets/VideoData/video_203.mp4', 'gaming,highlights'),
        (16, 'Gaming memes', '/home/favas/chameleo_app/assets/VideoData/video_204.mp4', 'gaming,comedy,memes,funny'),
        (17, 'Indie game', '/home/favas/chameleo_app/assets/VideoData/video_205.mp4', 'gaming,highlights'),
        (18, 'Retro gaming console', '/home/favas/chameleo_app/assets/VideoData/video_206.mp4', 'gaming,highlights'),
        (19, 'Speedrun', '/home/favas/chameleo_app/assets/VideoData/video_207.mp4', 'gaming,highlights'),
        (20, 'Video game easter eggs', '/home/favas/chameleo_app/assets/VideoData/video_208.mp4', 'gaming,highlights'),
        (21, 'Wukong review', '/home/favas/chameleo_app/assets/VideoData/video_209.mp4', 'gaming,review'),
        (22, '31 Random Movie Facts You Need To Know', '/home/favas/chameleo_app/assets/VideoData/video_301.mp4', 'movies,facts'),
        (23, 'Alia Bhatt And Vicky Kaushal The Whisper Challenge', '/home/favas/chameleo_app/assets/VideoData/video_302.mp4', 'celebs,interview'),
        (24, 'Aswanth Kok movie review', '/home/favas/chameleo_app/assets/VideoData/video_303.mp4', 'movies,review'),
        (25, 'Family Guy Funniest Moments Compilation', '/home/favas/chameleo_app/assets/VideoData/video_304.mp4', 'movies,funny,comedy,memes'),
        (26, 'Interstellar 4K HDR IMAX _ Into The Black Hole - Gargantua 1_2', '/home/favas/chameleo_app/assets/VideoData/video_305.mp4', 'movies,science,blackhole'),
        (27, 'Justin Bieber Entertainment news', '/home/favas/chameleo_app/assets/VideoData/video_306.mp4', 'celebs,news'),
        (28, 'Kannappa trailer', '/home/favas/chameleo_app/assets/VideoData/video_307.mp4', 'movies,trailer'),
        (29, 'Malayalam short film', '/home/favas/chameleo_app/assets/VideoData/video_308.mp4', 'movies,shortfilm'),
        (30, 'Marco bts', '/home/favas/chameleo_app/assets/VideoData/video_309.mp4', 'movies,bts'),
        (31, 'The Hangover Alans Funniest Moments', '/home/favas/chameleo_app/assets/VideoData/video_310.mp4', 'movies,funny,comedy,memes'),
        (32, 'top 5 badass action movies to watch now', '/home/favas/chameleo_app/assets/VideoData/video_311.mp4', 'movies,action'),
        (33, 'Best Drummer Ever [HD]', '/home/favas/chameleo_app/assets/VideoData/video_401.mp4', 'music,drum'),
        (34, 'BIllie Eilish music video bts', '/home/favas/chameleo_app/assets/VideoData/video_402.mp4', 'music,bts'),
        (35, 'ESSENTIAL GUITAR THEORY', '/home/favas/chameleo_app/assets/VideoData/video_403.mp4', 'music,guitar'),
        (36, 'Ghungroo _ James Combo Marino _ Hrithik Roshan _ War', '/home/favas/chameleo_app/assets/VideoData/video_404.mp4', 'dance,music'),
        (37, 'Guitar hero', '/home/favas/chameleo_app/assets/VideoData/video_405.mp4', 'music,guitar,gaming'),
        (38, 'Music memes', '/home/favas/chameleo_app/assets/VideoData/video_406.mp4', 'music,comedy,memes,funny'),
        (39, 'Bruno Mars Music videos', '/home/favas/chameleo_app/assets/VideoData/video_407.mp4', 'music,video'),
        (40, 'Not like us live', '/home/favas/chameleo_app/assets/VideoData/video_408.mp4', 'music,live'),
        (41, 'Painting tutorial', '/home/favas/chameleo_app/assets/VideoData/video_409.mp4', 'art,painting'),
        (42, 'Speed painting', '/home/favas/chameleo_app/assets/VideoData/video_410.mp4', 'art,painting'),
        (43, 'The Evolution of Animation (1833 – 2021),', '/home/favas/chameleo_app/assets/VideoData/video_411.mp4', 'art,movie'),
        (44, 'Yarrabah Music & Cultural Festival 2019 Highlights', '/home/favas/chameleo_app/assets/VideoData/video_412.mp4', 'music,festival'),
        (45, '27 Facts That Will Make You Question Your Existence', '/home/favas/chameleo_app/assets/VideoData/video_501.mp4', 'facts,science'),
        (46, 'American Bluebird builds nest masterpiece', '/home/favas/chameleo_app/assets/VideoData/video_502.mp4', 'animals,nature'),
        (47, 'Black hole', '/home/favas/chameleo_app/assets/VideoData/video_503.mp4', 'science,blackhole'),
        (48, 'Ocean Depth', '/home/favas/chameleo_app/assets/VideoData/video_504.mp4', 'science,nature'),
        (49, 'Quantum Mechanics Explained in Ridiculously Simple Words', '/home/favas/chameleo_app/assets/VideoData/video_505.mp4', 'science,education'),
        (50, 'Renewable Energy 101 _ National Geographic', '/home/favas/chameleo_app/assets/VideoData/video_506.mp4', 'science,education'),
        (51, 'Sandcat documentary', '/home/favas/chameleo_app/assets/VideoData/video_507.mp4', 'animals,nature,documentary'),
        (52, 'Science experiment in home', '/home/favas/chameleo_app/assets/VideoData/video_508.mp4', 'science,experiment'),
        (53, 'What Earth in 2050 could look like - Shannon Odell', '/home/favas/chameleo_app/assets/VideoData/video_509.mp4', 'science,education'),
        (54, 'Worlds smallest wild dog', '/home/favas/chameleo_app/assets/VideoData/video_510.mp4', 'animals,nature'),
        (55, 'Artificial intelligence introduction', '/home/favas/chameleo_app/assets/VideoData/video_601.mp4', 'tech,ai,science,education'),
        (56, 'Android Users react to iPhone 15 finally getting USB-C', '/home/favas/chameleo_app/assets/VideoData/video_602.mp4', 'tech,funny,comedy,memes'),
        (57, 'coding best practices', '/home/favas/chameleo_app/assets/VideoData/video_603.mp4', 'tech,coding,education'),
        (58, 'Cybersecurity basics', '/home/favas/chameleo_app/assets/VideoData/video_604.mp4', 'tech,cybersecurity,hacking,education'),
        (59, 'Cybersecurity introduction', '/home/favas/chameleo_app/assets/VideoData/video_605.mp4', 'tech,cybersecurity,hacking,education'),
        (60, 'Electroboom Funny Fail Compilation Part 1', '/home/favas/chameleo_app/assets/VideoData/video_606.mp4', 'tech,funny,comedy,memes'),
        (61, 'Flutter in 100 seconds', '/home/favas/chameleo_app/assets/VideoData/video_607.mp4', 'tech,flutter,education'),
        (62, 'Game development basics', '/home/favas/chameleo_app/assets/VideoData/video_608.mp4', 'tech,gaming,education'),
        (63, 'The Future of Robotics', '/home/favas/chameleo_app/assets/VideoData/video_609.mp4', 'tech,robotics,science'),
        (64, 'Web development roadmap', '/home/favas/chameleo_app/assets/VideoData/video_610.mp4', 'tech,web,education'),
        (65, 'What is internet of things', '/home/favas/chameleo_app/assets/VideoData/video_611.mp4', 'tech,iot,education'),
        (66, 'What is Python? Why Python is So Popular?', '/home/favas/chameleo_app/assets/VideoData/video_612.mp4', 'tech,python,education'),
        (67, '10 Essential Thailand Tips in 5 Minutes', '/home/favas/chameleo_app/assets/VideoData/video_701.mp4', 'travel,advice'),
        (68, 'Canada Road Trip_ Montreal to Vancouver in 5 minutes (2020),', '/home/favas/chameleo_app/assets/VideoData/video_702.mp4', 'travel,roadtrip'),
        (69, 'Food tour south india', '/home/favas/chameleo_app/assets/VideoData/video_703.mp4', 'food,travel'),
        (70, 'Hiking appalachian trail', '/home/favas/chameleo_app/assets/VideoData/video_704.mp4', 'travel,hiking'),
        (71, 'Peru in 10 Days_  A 6 MINUTE Travel Guide', '/home/favas/chameleo_app/assets/VideoData/video_705.mp4', 'travel,advice'),
        (72, 'The Ultimate Bungee Jumping Guide _ 5 Mins Travel Tips with Neil Patil', '/home/favas/chameleo_app/assets/VideoData/video_706.mp4', 'travel,adventure'),
        (73, 'Top 10 travel destinationss', '/home/favas/chameleo_app/assets/VideoData/video_707.mp4', 'travel,advice'),
        (74, 'Vacation Memes', '/home/favas/chameleo_app/assets/VideoData/video_708.mp4', 'travel,funny,comedy,memes')
    ]


    cursor.executemany("INSERT OR IGNORE INTO Videos (video_id, title, file_path, tags) VALUES (?, ?, ?, ?)", videos)
    
    interactions = [
        # User1 - Watches mostly tech and AI-related content
        ('user1', 0, 80.0),('user1', 1, 40.0),('user1', 9, 90.0),('user1', 14, 60.0),
        ('user1', 29, 85.0),('user1', 49, 75.0),('user1', 59, 35.0),('user1', 69, 95.0),
        ('user1', 54, 65.0),('user1', 24, 50.0),
        
        # User2 - Tech & AI with some interest in science
        ('user2', 0, 75.0),('user2', 2, 50.0),('user2', 9, 85.0),('user2', 19, 70.0),
        ('user2', 39, 45.0),('user2', 54, 90.0),('user2', 64, 30.0),('user2', 74, 95.0),
        ('user2', 34, 60.0),
        
        # User3 - Science & Space Enthusiast
        ('user3', 4, 60.0),('user3', 9, 85.0),('user3', 19, 50.0),('user3', 29, 40.0),
        ('user3', 44, 75.0),('user3', 54, 90.0),('user3', 67, 55.0),('user3', 73, 80.0),
        ('user3', 34, 50.0),('user3', 14, 85.0),
        
        # User4 - Gaming & AI
        ('user4', 1, 90.0),('user4', 4, 45.0),('user4', 14, 70.0),('user4', 24, 80.0),
        ('user4', 34, 50.0),('user4', 49, 65.0),('user4', 59, 30.0),('user4', 71, 85.0),
        ('user4', 9, 95.0),('user4', 19, 75.0),
        
        # User5 - Mixed interests (Tech, Science, Gaming)
        ('user5', 2, 75.0),('user5', 9, 40.0),('user5', 17, 90.0),('user5', 27, 55.0),
        ('user5', 37, 70.0),('user5', 57, 60.0),('user5', 62, 35.0),('user5', 72, 80.0),
        ('user5', 34, 50.0),('user5', 71, 90.0),
        
        # User6 - Science & Space with some travel
        ('user6', 0, 65.0),('user6', 6, 85.0),('user6', 16, 40.0),('user6', 21, 75.0),
        ('user6', 41, 50.0),('user6', 51, 90.0),('user6', 66, 35.0),('user6', 74, 95.0),
        ('user6', 71, 80.0),
        
        # User7 - Space, Science & Tech
        ('user7', 3, 50.0),('user7', 11, 70.0),('user7', 19, 90.0),('user7', 32, 65.0),
        ('user7', 46, 45.0),('user7', 52, 80.0),('user7', 63, 35.0),('user7', 71, 95.0),
        ('user7', 0, 60.0),('user7', 67, 85.0),
        
        # User8 - Food & Travel
        ('user8', 5, 60.0),('user8', 13, 85.0),('user8', 23, 50.0),('user8', 30, 40.0),
        ('user8', 45, 75.0),('user8', 55, 90.0),('user8', 68, 55.0),('user8', 73, 80.0),
        
        # User9 - Travel & Adventure
        ('user9', 1, 90.0),('user9', 7, 45.0),('user9', 18, 70.0),('user9', 28, 80.0),
        ('user9', 38, 50.0),('user9', 58, 65.0),('user9', 60, 30.0),('user9', 72, 85.0),
        ('user9', 74, 95.0),
        
        # User10 - Comedy & Travel mix
        ('user10', 8, 75.0),('user10', 12, 40.0),('user10', 20, 90.0),('user10', 33, 55.0),
        ('user10', 43, 70.0),('user10', 53, 60.0),('user10', 61, 35.0),('user10', 70, 80.0),
        
        # User11 - Food & Travel
        ('user11', 5, 50.0),('user11', 13, 80.0),('user11', 23, 90.0),('user11', 30, 60.0),
        ('user11', 45, 45.0),('user11', 55, 70.0),('user11', 68, 85.0),
        
        # User12 - Adventure & Sports
        ('user12', 10, 85.0),('user12', 25, 55.0),('user12', 35, 75.0),('user12', 48, 65.0),
        ('user12', 56, 90.0),('user12', 70, 40.0),('user12', 72, 95.0),
        
        # User13 - AI & Gaming
        ('user13', 1, 80.0),('user13', 14, 45.0),('user13', 24, 75.0),('user13', 37, 60.0),
        ('user13', 49, 90.0),('user13', 62, 55.0),('user13', 71, 85.0),
        
        # User14 - Comedy & Memes
        ('user14', 8, 65.0),('user14', 15, 80.0),('user14', 31, 40.0),('user14', 40, 75.0),
        ('user14', 50, 90.0),('user14', 65, 30.0),('user14', 74, 95.0),
        
        # User15 - Space & Science
        ('user15', 4, 75.0),('user15', 19, 85.0),('user15', 29, 90.0),('user15', 44, 55.0),
        ('user15', 54, 70.0),('user15', 67, 80.0),('user15', 73, 60.0)
    ]

    cursor.executemany("INSERT OR IGNORE INTO UserVideoInteraction (username, video_id, watch_percentage) VALUES (?, ?, ?)", interactions)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    insert_sample_data()
    print("Database setup complete.")
