from dao.PatientDao import PatientDao
from db.db_connection import DBConnection
from models.Patient import Patient
from datetime import datetime, date
from lib.PatientManagementLib import PatientManagementLib


class PatientDaoImpl(PatientDao):
    """MySQL-backed implementation of PatientDao."""

    # SQL statements aligned with schema from your ERD
    INSERT_SQL = (
        "INSERT INTO patients (patientid, name, dob, gender, bloodgroup, mobileno, address, isactive) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    )
    SELECT_ALL_SQL = (
        "SELECT patientid, name, dob, gender, bloodgroup, mobileno, address, isactive FROM patients ORDER BY patientid"
    )

    def __init__(self):
        self.conn = DBConnection().get_connection()

    def add_patient(self, patient: Patient):
        cursor = None
        try:
            cursor = self.conn.cursor()

            # Try to reuse the smallest missing patientid (gap) to keep IDs contiguous
            next_id = self._find_smallest_missing_id(cursor)

            try:
                cursor.execute(
                    self.INSERT_SQL,
                    (
                        next_id,  # may be None; MySQL treats NULL as auto-increment
                        patient.get_name(),
                        patient.get_dob(),
                        patient.get_gender(),
                        patient.get_bloodgroup(),
                        patient.get_mobileno(),
                        patient.get_address(),
                        'y' if patient.get_isactive() else 'n',
                    ),
                )
            except Exception as dup_err:
                # In rare race conditions, chosen id may be taken; fallback to auto-increment
                try:
                    cursor.execute(
                        self.INSERT_SQL,
                        (
                            None,
                            patient.get_name(),
                            patient.get_dob(),
                            patient.get_gender(),
                            patient.get_bloodgroup(),
                            patient.get_mobileno(),
                            patient.get_address(),
                            'y' if patient.get_isactive() else 'n',
                        ),
                    )
                except Exception:
                    raise dup_err

            self.conn.commit()
            return cursor.rowcount == 1, cursor.lastrowid
        except Exception as e:
            print("Error inserting patient:", e)
            self.conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def _find_smallest_missing_id(self, cursor):
        """
        Returns the smallest available positive integer patientid not used yet.
        If there are no gaps, returns None so that AUTO_INCREMENT is used.
        """
        try:
            # If 1 is free, use it first
            cursor.execute("SELECT 1 FROM patients WHERE patientid = 1 LIMIT 1")
            row = cursor.fetchone()
            if row is None:
                return 1

            # Find the smallest gap using self-join method
            cursor.execute(
                """
                SELECT MIN(t1.patientid) + 1 AS candidate
                FROM patients t1
                LEFT JOIN patients t2
                  ON t2.patientid = t1.patientid + 1
                WHERE t2.patientid IS NULL
                """
            )
            res = cursor.fetchone()
            if res and res[0] is not None:
                # Verify that candidate is greater than 0
                return int(res[0]) if int(res[0]) > 0 else None
        except Exception:
            # On any error, gracefully fallback to auto-increment
            return None
        return None

    def get_patient_by_id(self, patient_id):
        cursor = None
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM patients WHERE patientid = %s", (patient_id,))
            row = cursor.fetchone()
            if row:
                # Normalize DB values to match validators
                raw_dob = row.get("dob")
                if isinstance(raw_dob, (datetime, date)):
                    dob_str = raw_dob.strftime("%Y-%m-%d")
                else:
                    dob_str = str(raw_dob) if raw_dob is not None else ""

                mobileno_str = str(row.get("mobileno", ""))
                gender_str = str(row.get("gender", "")).strip()
                bloodgroup_str = str(row.get("bloodgroup", "")).strip()
                is_active_bool = True if str(row.get("isactive", "y")).lower() in ("y", "true", "1") else False

                # Fallbacks for legacy/nullable data
                if not PatientManagementLib.validate_dob(dob_str):
                    dob_str = "1970-01-01"
                if not PatientManagementLib.validate_gender(gender_str):
                    gender_str = "other"
                if not PatientManagementLib.validate_bloodgroup(bloodgroup_str):
                    bloodgroup_str = "O+"
                if not PatientManagementLib.validate_mobile(mobileno_str):
                    mobileno_str = "6000000000"
                address_str = row.get("address", "") or ""
                if not PatientManagementLib.validate_address(address_str):
                    address_str = "Unknown Address"

                return Patient(
                    row["patientid"],
                    row["name"],
                    dob_str,
                    gender_str,
                    bloodgroup_str,
                    mobileno_str,
                    address_str,
                    is_active_bool,
                )
        except Exception as e:
            print("Error fetching patient:", e)
        finally:
            if cursor:
                cursor.close()
        return None

    def delete_patient(self, patient_id):
        cursor = None
        try:
            cursor = self.conn.cursor()
            # Update isactive to 'n' for soft delete
            cursor.execute("UPDATE patients SET isactive = 'n' WHERE patientid = %s AND isactive = 'y'", (patient_id,))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Error deactivating patient:", e)
            self.conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def update_patient(self, patient):
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """UPDATE patients 
                   SET name = %s, dob = %s, gender = %s, bloodgroup = %s, 
                       mobileno = %s, address = %s, isactive = %s 
                   WHERE patientid = %s""",
                (
                    patient.get_name(),
                    patient.get_dob(),
                    patient.get_gender(),
                    patient.get_bloodgroup(),
                    patient.get_mobileno(),
                    patient.get_address(),
                    'y' if patient.get_isactive() else 'n',
                    patient.get_patientid(),
                ),
            )
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Error updating patient:", e)
            self.conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def update_patient_status(self, patient_id, is_active):
        """Update the active status of a patient"""
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "UPDATE patients SET isactive = %s WHERE patientid = %s",
                ('y' if is_active else 'n', patient_id)
            )
            self.conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating patient status: {e}")
            self.conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def list_patients(self, include_inactive=False):
        cursor = None
        patients = []
        try:
            cursor = self.conn.cursor(dictionary=True)
            if include_inactive:
                cursor.execute(self.SELECT_ALL_SQL)
            else:
                cursor.execute("""
                    SELECT patientid, name, dob, gender, bloodgroup, mobileno, address, isactive 
                    FROM patients 
                    WHERE isactive = 'y' 
                    ORDER BY patientid
                """)
            rows = cursor.fetchall()
            for r in rows:
                # Normalize DB values to match validators
                raw_dob = r.get("dob")
                if isinstance(raw_dob, (datetime, date)):
                    dob_str = raw_dob.strftime("%Y-%m-%d")
                else:
                    dob_str = str(raw_dob) if raw_dob is not None else ""

                mobileno_str = str(r.get("mobileno", ""))
                gender_str = str(r.get("gender", "")).strip()
                bloodgroup_str = str(r.get("bloodgroup", "")).strip()
                is_active_bool = str(r.get("isactive", "y")).lower() in ("y", "true", "1")

                # Fallbacks for legacy/nullable data to avoid listing failures
                if not PatientManagementLib.validate_dob(dob_str):
                    dob_str = "1970-01-01"
                if not PatientManagementLib.validate_gender(gender_str):
                    gender_str = "other"
                if not PatientManagementLib.validate_bloodgroup(bloodgroup_str):
                    bloodgroup_str = "O+"
                if not PatientManagementLib.validate_mobile(mobileno_str):
                    mobileno_str = "6000000000"
                address_str = r.get("address", "") or ""
                if not PatientManagementLib.validate_address(address_str):
                    address_str = "Unknown Address"

                patients.append(
                    Patient(
                        r["patientid"],
                        r["name"],
                        dob_str,
                        gender_str,
                        bloodgroup_str,
                        mobileno_str,
                        address_str,
                        is_active_bool,
                    )
                )
        except Exception as e:
            print("Error fetching patients:", e)
        finally:
            if cursor:
                cursor.close()
        return patients
