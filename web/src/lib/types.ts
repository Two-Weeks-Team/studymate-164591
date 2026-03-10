export interface Topic {
  topic_id: string;
  name: string;
  study_days: string[]; // ISO dates
  completion_status: boolean;
}

export interface StudyPlan {
  plan_id: string;
  user_id: string;
  topics: Topic[];
  start_date: string;
  end_date: string;
}

export interface RevisionCard {
  card_id: string;
  user_id: string;
  front: string;
  back: string;
  last_reviewed: string;
}
