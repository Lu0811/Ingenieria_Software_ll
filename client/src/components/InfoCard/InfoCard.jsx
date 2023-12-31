import React, { useEffect, useState, useRef } from "react";
import "./InfoCard.css";
import { UilPen } from "@iconscout/react-unicons";
import ProfileModal from "../ProfileModal/ProfileModal";
import { useDispatch, useSelector } from "react-redux";
import { useParams } from "react-router-dom";
import * as UserApi from "../../api/UserRequests.js";
import { logout } from "../../actions/AuthActions";

const InfoCard = () => {
  const dispatch = useDispatch();
  const params = useParams();
  const [modalOpened, setModalOpened] = useState(false);
  const profileUserId = params.id;
  const [profileUser, setProfileUser] = useState({});
  const isMounted = useRef(true);

  const user = useSelector((state) => state.authReducer.authData);

  const handleLogOut = () => {
    dispatch(logout());
  };

  useEffect(() => {
    const fetchProfileUser = async () => {
      isMounted.current = true;
      if (profileUserId === user.id.toString()) {
        setProfileUser(user);
      } else {
        console.log("fetching");
        const profileUser = await UserApi.getUser(profileUserId);
        if (isMounted.current) {
          setProfileUser(profileUser);
        }
        console.log(profileUser);
      }
    };
    fetchProfileUser();
    return () => {
      isMounted.current = false;
    };
  }, [profileUserId, user]);

  return (
    <div className="InfoCard">
      <div className="infoHead">
        <h4>Profile Info</h4>
        {user.id.toString() === profileUserId ? (
          <div>
            <UilPen
              width="2rem"
              height="1.2rem"
              onClick={() => setModalOpened(true)}
            />

            <ProfileModal
              modalOpened={modalOpened}
              setModalOpened={setModalOpened}
              data={user}
            />
          </div>
        ) : (
          ""
        )}
      </div>

      <div className="info">
        {/* */}
        <span>
          <b>Estado </b>
        </span>
        <span>{profileUser.relationship}</span>
      </div>
      <div className="info">
        <span>
          <b>Vive en </b>
        </span>
        <span>{profileUser.livesIn}</span>
      </div>
      <div className="info">
        <span>
          <b>Trabaja en </b>
        </span>
        <span>{profileUser.worksAt}</span>
      </div>

      <button className="button logout-button" onClick={handleLogOut}>
        Log Out
      </button>
    </div>
  );
};

export default InfoCard;
