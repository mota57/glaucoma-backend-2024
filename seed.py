from config import GlaucomaConfig
from models import file_status, patient_file, user_type, user_account, Base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select

engine = create_engine(GlaucomaConfig.DB_CONNECTION, echo=True)

def seed_data():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    fill_status_and_type()
    with Session(engine) as session:
        doctor_user_type = session.scalars(select(user_type).filter_by(name="doctor")).first()
        # set doctor
        doctor = user_account(first_name="carlos", last_name="loyola", 
                                 user_type_id = doctor_user_type.user_type_id)
        # adding doctor
        session.add(doctor)
        session.commit()
        print('adding doctor')
        # get patient by user type patient
        patient_user_type = session.scalars(select(user_type).filter_by(name="patient")).first()
        # create patient
        patient = user_account(first_name="carlos", last_name="loyola", 
                                 user_type_id = patient_user_type.user_type_id)
        # adding patient to doctor
        patient.patient_doctor_id = doctor.user_account_id
        session.add(patient)
        session.commit()

        print(f'adding patient {patient!r} to doctor: {doctor!r}')
        if patient.user_account_id > 0:
            # get  processing file
            processing_file_status = session.scalars(select(file_status).filter_by(name="processing")).first()
            print(f'pull from db file_status: {processing_file_status.name!r}')
            file_test = patient_file(file_status_id=processing_file_status.file_status_id, 
                                    path="https://glaucoma-website-107594336623.s3.amazonaws.com/images/EyePACS-TRAIN-NRG-2887.jpg", 
                                    user_account_id=patient.user_account_id)
            session.add(file_test)
            session.commit()
            print(f'adding file {file_test.path!r} to db')
        else:
            print('warning patient.user_account_id == 0')

def fill_status_and_type():
    with Session(engine) as session:
        # create file status
        session.add_all([
            file_status(name="enqueue"),
            file_status(name="processing"),
            file_status(name="success"),
            file_status(name="error")
        ])
        print('adding file_status')
        session.commit()
        # adding user type
        session.add_all([
            user_type(name="doctor"),
            user_type(name="patient"),
        ])
        print('adding user_types')
        session.commit()


if __name__ == '__main__':
    seed_data()