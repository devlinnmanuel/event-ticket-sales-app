import mysql.connector
from tkinter import messagebox

class SQL:
    def __init__(self):
        self.connect_SQL()

    def connect_SQL(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="DevSQL265Man**"
            )

            if self.conn.is_connected():
                self.cursor = self.conn.cursor()
                self.cursor.execute("CREATE DATABASE IF NOT EXISTS events_db")
                self.conn.database = 'events_db'

                if self.not_created():
                    self.cursor.execute("""
                        CREATE TABLE IF NOT EXISTS event (
                        event_id VARCHAR(20) PRIMARY KEY,
                        event_name VARCHAR(100) NOT NULL,
                        schedule TEXT NOT NULL,
                        events_detail TEXT NOT NULL,
                        price DECIMAL(10,2) NOT NULL,
                        event_photo TEXT NOT NULL,
                        status enum('comming soon', 'passed') NOT NULL,
                        genre VARCHAR(100) NOT NULL
                        );
                        """)
                    
                    self.cursor.execute("""
                        CREATE TABLE IF NOT EXISTS event_attribute (
                        event_id VARCHAR(20),
                        symphony INT NOT NULL,
                        concerto INT NOT NULL,
                        orchestral INT NOT NULL,
                        chamber  INT NOT NULL,
                        choral INT NOT NULL,
                        ballet INT NOT NULL,
                        themed INT NOT NULL
                        );
                        """)
                    
                    self.cursor.execute("""
                        CREATE TABLE IF NOT EXISTS account (
                        account_id VARCHAR(200) NOT NULL,
                        first_name VARCHAR(100) NOT NULL, 
                        last_name VARCHAR(100) NOT NULL, 
                        username VARCHAR(100) NOT NULL,  
                        password VARCHAR(100) NOT NULL,  
                        email VARCHAR(100) NOT NULL,  
                        wallet INT NOT NULL
                        )
                        """)

                    self.cursor.execute("""
                        CREATE TABLE IF NOT EXISTS ticket (
                        ticket_id VARCHAR(20) NOT NULL,
                        account_id VARCHAR(20) NOT NULL,
                        event_id VARCHAR(20) NOT NULL,
                        quantity INT NOT NULL
                        )
                        """)

                    self.cursor.execute(r"""
                        INSERT INTO account (account_id, first_name, last_name, username, password, email, wallet) VALUES
                            ('A001','Alice', 'Smith', 'alice123', '4', 'alice@example.com', 500),
                            ('A002','Bob', 'Johnson', 'bobj', 'password2', 'bob@example.com', 600),
                            ('A003','Charlie', 'Brown', 'charlieb', 'password3', 'charlie@example.com', 400),
                            ('A004','Diana', 'Prince', 'dianap', 'password4', 'diana@example.com', 540),
                            ('A005','Evan', 'Thomas', 'evant', 'password5', 'evan@example.com', 630),
                            ('A006','Fiona', 'Williams', 'fionaw', 'password6', 'fiona@example.com', 20),
                            ('A007','George', 'Martin', 'georgem', 'password7', 'george@example.com', 2000),
                            ('A008','Hannah', 'Wilson', 'hannahw', 'password8', 'hannah@example.com', 5),
                            ('A009','Ivan', 'Peterson', 'ivanp', 'password9', 'ivan@example.com', 0),
                            ('A010','Julia', 'Roberts', 'juliar', 'password10', 'julia@example.com', 1000);
                    """)

                    self.conn.commit()
                    self.cursor.execute(r"""
                        INSERT INTO event (event_id, event_name, schedule, events_detail, price, event_photo, status, genre) VALUES
                            ('E001', 'Beethoven Symphony No.9', '2024-12-05 19:30:00', 'Experience the monumental grandeur of Ludwig van Beethoven\'s Symphony No. 9, a pinnacle of classical music that transcends time and genre. Premiered in 1824, this symphony stands as Beethoven\'s final complete symphonic work and is renowned for its innovative structure and profound emotional depth. The symphony unfolds in four movements, seamlessly blending orchestral mastery with choral brilliance in the final movement\'s iconic "Ode to Joy." This groundbreaking inclusion of vocal soloists and a full chorus within a symphonic framework broke new ground, symbolizing universal brotherhood and human solidarity. The Ninth Symphony not only showcases Beethoven\'s genius in thematic development and orchestration but also serves as a timeless testament to the enduring power of music to inspire and unify humanity.', 120.00, "imgs/Beethoven9.jpeg", 1,'Choral'),
                            ('E002', 'Mozart Requiem', '2024-11-20 19:00:00', 'Delve into the profound spiritual and emotional depths of Wolfgang Amadeus Mozart\'s Requiem, a masterpiece shrouded in mystery and legend. Composed in the final year of Mozart\'s life, this unfinished work was posthumously completed by his student Franz Xaver Süssmayr. The Requiem Mass in D minor is a sublime fusion of sublime melodies, intricate counterpoint, and dramatic contrasts, reflecting the composer\'s own contemplation of mortality and the afterlife. Each movement—from the solemn "Introitus" to the triumphant "Lux Aeterna"—offers a unique exploration of faith, sorrow, and hope. Mozart\'s Requiem remains a cornerstone of sacred music, celebrated for its emotional intensity and profound beauty, inviting listeners to a deeply reflective and transcendent musical journey.', 150.00, "imgs/mozart_requiem.jpeg", 1,'Choral'),
                            ('E003', 'Vivaldi Four Seasons', '2024-12-15 18:30:00', 'Embark on a vibrant and evocative journey through the changing seasons with Antonio Vivaldi\'s "The Four Seasons," a groundbreaking set of four violin concertos that paint vivid musical landscapes of spring, summer, autumn, and winter. Composed in 1723, each concerto is intricately crafted to depict the unique characteristics and moods of its respective season, blending Baroque elegance with programmatic innovation. The "Spring" bursts with lively melodies and pastoral tranquility, while "Summer" conveys the intensity and turbulence of a storm. "Autumn" celebrates harvest and merriment, and "Winter" captures the stark beauty and biting cold of the season. Vivaldi\'s masterful interplay between soloist and orchestra, combined with his imaginative use of musical motifs, makes "The Four Seasons" a timeless favorite that continues to enchant audiences with its vivid storytelling and exquisite craftsmanship.', 130.00, "imgs/four_seasons.jpeg", 1,'Concerto'),
                            ('E004', 'Handel Messiah', '2024-12-20 20:00:00', 'Celebrate the divine with George Frideric Handel\'s "Messiah," an oratorio of unparalleled grandeur and spiritual resonance. Premiered in 1742, this seminal work is structured in three parts, chronicling the prophecy, life, death, and resurrection of Jesus Christ. Handel\'s masterful composition weaves together a rich tapestry of choral harmonies, soaring arias, and dynamic orchestration, creating a profound narrative that has moved audiences for centuries. Highlights include the majestic "Hallelujah Chorus," the tender "He Was Despised," and the triumphant "I Know That My Redeemer Lives." "Messiah" transcends religious boundaries, offering a universal message of hope, redemption, and the enduring power of faith. Whether performed in grand concert halls or intimate settings, Handel\'s "Messiah" remains a cornerstone of choral repertoire, celebrated for its emotional depth and sublime beauty.', 100.00, "imgs/handels_messiah.jpeg", 1, 'Choral'),
                            ('E005', 'Tchaikovsky Nutcracker', '2024-12-23 19:00:00', 'Immerse yourself in the enchanting world of Pyotr Ilyich Tchaikovsky\'s "The Nutcracker," a timeless ballet that has become synonymous with the magic of the holiday season. Premiered in 1892, this beloved work transports audiences to a fantastical realm where dreams and reality intertwine. The story follows young Clara as she embarks on a wondrous journey with her Nutcracker Prince, encountering a host of magical characters, from the Sugar Plum Fairy to the mischievous Mouse King. Tchaikovsky\'s score is a masterpiece of melodic brilliance and orchestral color, featuring iconic pieces such as the "Dance of the Sugar Plum Fairy," the "Waltz of the Flowers," and the exuberant "March." The "Nutcracker" is celebrated for its exquisite choreography, dazzling sets, and the seamless fusion of music and narrative, making it a perennial favorite that delights audiences of all ages with its charm and elegance.', 160.00, "imgs/nutcracker.jpeg", 2, 'Themed Event'),
                            ('E007', 'Schubert Symphony No. 8', '2024-11-30 19:30:00', 'Delve into the mysterious beauty of Franz Schubert\'s Symphony No. 8, famously known as the "Unfinished Symphony." Composed in 1822, this enigmatic work consists of only two completed movements, yet it has captivated audiences for centuries with its lyrical depth and emotional poignancy. The symphony opens with a brooding Allegro moderato, characterized by its haunting themes and rich harmonic textures, followed by the serene and lyrical Andante con moto, which showcases Schubert\'s gift for melody and orchestration. Despite its incomplete status, the "Unfinished Symphony" is celebrated as a masterpiece of Romantic music, embodying Schubert\'s ability to convey profound emotion and introspection through his distinctive musical voice.', 110.00, "imgs/schubert_symphony_8.jpeg", 1, 'Symphony'),
                            ('E008', 'Chopin Piano Concerto', '2024-12-02 18:00:00', 'Immerse yourself in the sublime elegance of Frédéric Chopin\'s Piano Concerto No. 1, a cornerstone of the Romantic repertoire that showcases the composer\'s unparalleled genius for the piano. Premiered in 1830, this concerto is a virtuosic showcase of dazzling technique and lyrical beauty, with the piano taking center stage in a dialogue with a rich orchestral accompaniment. The first movement, Allegro maestoso, bursts with youthful energy and sweeping themes, while the Larghetto offers a tender and introspective interlude. The final Rondo brings the concerto to a spirited and triumphant conclusion. Chopin\'s Piano Concerto is celebrated for its expressive range, intricate melodies, and emotional depth, offering audiences a captivating journey through the heart of Romantic piano music.', 135.00, "imgs/chopin_piano.jpeg", 1, 'Concerto'),
                            ('E009', 'Rachmaninoff Piano Concerto No.2', '2024-12-18 20:00:00', 'Experience the profound emotional power and technical brilliance of Sergei Rachmaninoff\'s Piano Concerto No. 2, a masterpiece that has become one of the most beloved works in the Romantic piano repertoire. Composed in 1901, this concerto is a testament to Rachmaninoff\'s resilience and creativity, marking his triumphant return to composition after a period of self-doubt. The concerto opens with dramatic chords that lead into a sweeping, lyrical theme, setting the tone for the work\'s passionate and expressive character. The second movement, Adagio sostenuto, is a tender and introspective meditation, while the final movement bursts with virtuosic energy and triumphant resolve. Rachmaninoff\'s Piano Concerto No. 2 continues to captivate audiences with its lush harmonies, unforgettable melodies, and deeply moving emotional narrative.', 150.00, "imgs/rach_2.jpeg", 1, 'Concerto'),
                            ('E010', 'Debussy La Mer', '2024-11-15 19:00:00', 'Dive into the mesmerizing world of Claude Debussy\'s "La Mer," an orchestral masterpiece that captures the dynamic beauty and mystery of the sea. Composed between 1903 and 1905, this three-movement work is a cornerstone of Impressionist music, showcasing Debussy\'s innovative use of orchestral color and texture. "La Mer" opens with "From Dawn to Noon on the Sea," a shimmering depiction of the ocean\'s awakening, followed by "Play of the Waves," a lively and intricate interplay of themes and rhythms. The final movement, "Dialogue of the Wind and the Sea," builds to a powerful and dramatic climax. Debussy\'s "La Mer" invites listeners on an immersive journey through the ever-changing moods and majesty of the sea, offering a transformative musical experience.', 125.00, "imgs/debussy_la_mer.jpeg", 2, 'Symphony'),
                            ('E011', 'Shostakovich Symphony No.7', '2024-11-15 19:00:00', 'Discover the monumental power of Dmitri Shostakovich\'s Symphony No. 7, also known as the "Leningrad Symphony," a work that embodies resilience and defiance in the face of adversity. Composed during the siege of Leningrad in World War II, this symphony is a profound tribute to the human spirit and a stirring call for hope and unity. The first movement features the famous "Invasion Theme," a relentless and ominous motif that grows in intensity, symbolizing the encroaching forces of war. The symphony unfolds with haunting beauty and dramatic contrasts, culminating in a triumphant finale that celebrates the indomitable will to overcome. Shostakovich\'s Symphony No. 7 remains a powerful testament to the enduring strength of art and humanity.', 125.00, "imgs/Shost 7.png", 2, 'Symphony'),
                            ('E012', 'Mahler Symphony No. 5', '2024-11-25 19:30:00', 'Embark on an emotional odyssey with Gustav Mahler\'s Symphony No. 5, a monumental work that explores the depths of human experience through its powerful and deeply personal music. Composed between 1901 and 1902, this symphony is renowned for its dramatic narrative arc, beginning with a somber funeral march and culminating in a jubilant celebration of life. The Adagietto, the fourth movement, is one of Mahler\'s most famous compositions, a poignant and lyrical expression of love and longing. With its intricate orchestration, profound emotional depth, and sweeping themes, Mahler\'s Symphony No. 5 continues to captivate audiences as a masterwork of the symphonic repertoire.', 140.00, "imgs/Mahler 2.jpg", 1, 'Symphony'),
                            ('E013', 'Strauss Also sprach Zarathustra', '2024-12-10 20:00:00', 'Experience the awe-inspiring grandeur of Richard Strauss\'s "Also sprach Zarathustra," a symphonic tone poem inspired by Friedrich Nietzsche\'s philosophical novel. Composed in 1896, this work is best known for its iconic opening fanfare, "Sunrise," which has become one of the most recognizable pieces in classical music. Strauss\'s masterful orchestration captures the existential themes and cosmic vision of Nietzsche\'s work, unfolding in a series of contrasting sections that explore humanity\'s quest for meaning and transcendence. From its majestic beginnings to its contemplative conclusion, "Also sprach Zarathustra" is a testament to Strauss\'s brilliance as a composer and his ability to convey profound ideas through music.', 150.00, "imgs/strauss.jpeg", 1, 'Symphony'),
                            ('E014', 'Prokofiev Romeo and Juliet', '2024-12-08 19:00:00', 'Relive the timeless tale of love and tragedy with Sergei Prokofiev\'s "Romeo and Juliet," a ballet score that captures the essence of Shakespeare\'s immortal story. Composed in 1935, this work is celebrated for its vivid characterizations, dramatic intensity, and lush melodies. Highlights include the poignant "Montagues and Capulets," the tender "Balcony Scene," and the heartrending "Death of Juliet." Prokofiev\'s innovative use of orchestration and his ability to convey deep emotion make this score a masterpiece of 20th-century music, offering audiences a powerful and unforgettable musical experience.', 135.00, "imgs/Romeo Juliet.jpeg", 2, 'Concerto'),
                            ('E015', 'Ravel Boléro', '2024-11-22 18:30:00', 'Be mesmerized by the hypnotic and ever-intensifying rhythms of Maurice Ravel\'s "Boléro," a singular masterpiece that has captivated audiences since its premiere in 1928. Originally composed as a ballet, "Boléro" is built on a single, insistent melody that repeats and evolves over the course of the work, gradually building in volume and complexity. Ravel\'s ingenious orchestration adds layer upon layer of texture, culminating in a breathtaking climax that leaves listeners spellbound. "Boléro" is a celebration of musical minimalism and innovation, showcasing Ravel\'s extraordinary talent for crafting an unforgettable auditory journey.', 120.00, "imgs/Balero.jpg", 1, 'Concerto');
                    """)

                    self.conn.commit()
                    self.cursor.execute(rf"""
                        INSERT INTO ticket (ticket_id, account_id, event_id, quantity) VALUES
                            ('T001', 'A001', 'E001', 2),
                            ('T002', 'A002', 'E002', 1),
                            ('T003', 'A005', 'E003', 3),
                            ('T004', 'A003', 'E004', 1),
                            ('T005', 'A001', 'E005', 2),
                            ('T006', 'A003', 'E006', 1),
                            ('T007', 'A009', 'E007', 2),
                            ('T008', 'A001', 'E008', 1),
                            ('T009', 'A007', 'E009', 3),
                            ('T010', 'A005', 'E010', 1);
                    """)

                    self.cursor.execute(rf"""
                        INSERT INTO event_attribute (event_id, symphony, concerto,orchestral , chamber, choral, ballet, themed) VALUES
                            ('E001', 1, 0, 1, 0, 1, 0, 0),
                            ('E002', 0, 0, 1, 0, 1, 0, 0),
                            ('E003', 0, 1, 1, 1, 0, 0, 0),
                            ('E004', 0, 0, 1, 0, 0, 0, 0),
                            ('E005', 0, 0, 1, 0, 0, 1, 1),
                            ('E007', 1, 0, 1, 0, 0, 0, 0),
                            ('E008', 0, 1, 1, 0, 0, 0, 0),
                            ('E009', 0, 1, 1, 0, 0, 0, 0),
                            ('E010', 0, 0, 1, 0, 0, 0, 1),
                            ('E011', 1, 0, 1, 0, 0, 0, 0),
                            ('E012', 1, 0, 1, 0, 0, 0, 0),
                            ('E013', 0, 0, 1, 0, 0, 0, 1),
                            ('E014', 0, 0, 1, 0, 0, 1, 1),
                            ('E015', 0, 0, 1, 0, 0, 0, 1);
                    """)
                    
                self.conn.commit()

        except mysql.connector.Error as e:
            print(f"Error: {e}")
        finally:
            return self.conn, self.cursor

    def update_data(self, table, id, column, value):
        self.cursor.execute("START TRANSACTION")
        self.cursor.execute(f"""
            UPDATE {table} 
            SET {column} = {value}
            WHERE {table}_id = '{id}'
        """)
        self.cursor.execute("COMMIT")

    def update_all_events_state(self):
        self.cursor.execute("START TRANSACTION")
        self.cursor.execute("""
                UPDATE event
                SET status = CASE 
                    WHEN schedule > NOW() THEN 'comming soon'
                    WHEN schedule < NOW() THEN 'passed'
                    ELSE status
                END;
            """)
        self.cursor.execute("COMMIT")

    def delete_data(self, table, id):
        self.cursor.execute("START TRANSACTION")
        self.cursor.execute(f"""
            DELETE
            FROM {table}
            WHERE {table}_id = '{id}'
        """)
        self.cursor.execute("COMMIT")

    def select_ticket(self, user):
        self.cursor.execute(f"""
            SELECT ticket_id, 
            account.account_id, first_name, last_name, username, password, email, wallet, 
            event.event_id, event_name, price, events_detail, event_photo, schedule, status, genre,
            quantity FROM ticket
            JOIN account ON (account.account_id = ticket.account_id)
            JOIN event ON (event.event_id = ticket.event_id)
            WHERE account.account_id = '{user}'               
            ORDER BY (ticket_id)
        """)

        return self.cursor.fetchall()

    def select_all_ticket(self):
        self.cursor.execute(f"""
            SELECT ticket_id, 
            account.account_id, first_name, last_name, username, password, email, wallet, 
            event.event_id, event_name, price, events_detail, event_photo, schedule, status,genre,
            quantity FROM ticket
            JOIN account ON (account.account_id = ticket.account_id)
            JOIN event ON (event.event_id = ticket.event_id)
            ORDER BY (ticket_id)
        """)
        return self.cursor.fetchall()

    def select_all(self, table_name):
        self.cursor.execute(f"SELECT * FROM {table_name}")
        results = self.cursor.fetchall()
        return results
    
    def select_attribute(self, event_id):
        self.cursor.execute(f"""
            SELECT symphony, concerto, orchestral, chamber, choral, ballet, themed
            FROM event_attribute
            WHERE event_id = '{event_id}'
            """)
        return self.cursor.fetchall()[0]
    
    def select_attributes(self):
        self.cursor.execute(f"""
            SELECT symphony, concerto, orchestral, chamber, choral, ballet, themed
            FROM event_attribute
            """)
        return self.cursor.fetchall()

    def add_event(self, event_id, event_name, schedule, events_detail, price, event_photo, status):
        self.cursor.execute(
            "INSERT INTO event (event_id, event_name, schedule, events_detail, price, event_photo, status, genre) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (event_id, event_name, schedule, events_detail, price, event_photo, status))
        self.conn.commit()

    def add_account(self, account_id, first_name, last_name, username, password, email, wallet):
        self.cursor.execute(
            "INSERT INTO account (account_id, first_name, last_name, username, password, email, wallet) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (account_id, first_name, last_name, username, password, email, wallet))
        self.conn.commit()

    def add_ticket(self, ticket_id, account_id, event_id, quantity):
        self.cursor.execute(
            "INSERT INTO ticket (ticket_id, account_id, event_id, quantity) VALUES (%s, %s, %s, %s)",
            (ticket_id, account_id, event_id, quantity))
        self.conn.commit()

    def save_updated_profile(self, account_id, first_name, last_name, username, password, email):
        self.cursor.execute("""
                UPDATE account
                SET first_name = %s, last_name = %s, username = %s, password = %s, email = %s
                WHERE account_id = %s
            """, (first_name, last_name, username, password, email, account_id))

        self.conn.commit()

    def get_ticket_id(self, account_id, event_id):
        try:
            self.cursor.execute("""
                    SELECT ticket_id FROM ticket
                    WHERE account_id = %s AND event_id = %s
                """, (account_id, event_id))
            result = self.cursor.fetchall()

            return result

        except Exception as e:
            print(f"Error retrieving ticket_id: {e}")
            return []

    def not_created(self):
        self.cursor.execute("SHOW TABLES")
        return len(self.cursor.fetchall()) == 0
